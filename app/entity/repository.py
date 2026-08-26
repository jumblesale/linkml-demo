from sqlalchemy import UniqueConstraint, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Table
from typing import cast

from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.entity import Base
from bookstore.generated.schema import RelationshipMetadata, SchemaClassAddressable
from app.entity.id import Identifier
from app.entity.mappers import DomainEntityConverter
from app.entity.exceptions import (
    EntityNotFound,
    RelatedEntityNotFound,
    UniqueConstraintViolation,
)


class EntityRepository:
    def __init__(self, session: Session):
        self.converter = DomainEntityConverter()
        self.session = session

    def save(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
    ) -> None:
        entity = self.converter.to_entity(
            schema_class,
            domain,
            relationship_values=self._resolve_relationships(schema_class, domain),
        )
        try:
            self.session.add(entity)
            self.session.flush()
        except IntegrityError as error:
            if not self._is_unique_violation(error):
                raise
            field = self._unique_field(entity, error)
            raise UniqueConstraintViolation(field) from error

    def delete(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> None:
        existing_entity = self.session.get(
            schema_class.entity_class,
            entity_id,
        )
        if existing_entity is None:
            raise EntityNotFound(schema_class.entity_name(), entity_id)
        self.session.delete(existing_entity)

    def _resolve_relationships(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
    ) -> dict[str, object]:
        orm_relationship_names = set(
            schema_class.entity_class.__mapper__.relationships.keys()
        )
        return {
            name: self._resolve_relationship(
                name,
                relationship,
                getattr(domain, name),
            )
            for name, relationship in schema_class.relationships.items()
            if name in orm_relationship_names
            and getattr(domain, name, None) is not None
        }

    def _resolve_relationship(
        self,
        name: str,
        relationship: RelationshipMetadata,
        value: Identifier | list[Identifier],
    ) -> object:
        target_schema_class = self._target_schema_class(
            relationship.target_class_name
        )
        values = value if isinstance(value, list) else [value]
        related_entities = [
            self._find_related_entity(
                name,
                target_schema_class,
                related_value,
            )
            for related_value in values
        ]
        return (
            related_entities
            if relationship.multivalued
            else related_entities[0]
        )

    def _find_related_entity(
        self,
        relationship_name: str,
        target_schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> Base:
        entity = self.session.get(
            target_schema_class.entity_class,
            str(entity_id),
        )
        if entity is None:
            raise RelatedEntityNotFound(relationship_name, str(entity_id))
        return entity

    @staticmethod
    def _target_schema_class(
        target_class_name: str,
    ) -> type[SchemaClassAddressable]:
        for schema_class in SchemaClassAddressable.__subclasses__():
            if schema_class.__name__ == target_class_name:
                return schema_class
        raise LookupError(f"Unknown relationship target '{target_class_name}'")

    @staticmethod
    def _is_unique_violation(error: IntegrityError) -> bool:
        message = str(error.orig).lower()
        return "unique constraint" in message or "duplicate key" in message

    @staticmethod
    def _unique_field(entity: Base, error: IntegrityError) -> str:
        constraint_name = getattr(
            getattr(error.orig, "diag", None),
            "constraint_name",
            None,
        )
        table = cast(Table, entity.__table__)
        for constraint in table.constraints:
            if (
                isinstance(constraint, UniqueConstraint)
                and constraint.name == constraint_name
            ):
                return next(iter(constraint.columns)).name
        return constraint_name or "unknown"

    def find_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DomainModel]:
        entities = self.session.scalars(select(schema_class.entity_class)).all()
        return [
            self.converter.to_domain(schema_class, entity)
            for entity in entities
        ]

    def find_by_id(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> DomainModel | None:
        entity = self.session.get(schema_class.entity_class, entity_id)
        if entity is None:
            return None
        return self.converter.to_domain(schema_class, entity)
