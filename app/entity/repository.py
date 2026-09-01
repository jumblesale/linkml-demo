from typing import cast

from sqlalchemy import UniqueConstraint, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Table

from app.entity.exceptions import (
    EntityNotFound,
    RelatedEntityNotFound,
    UniqueConstraintViolation,
)
from app.entity.id import Identifier
from app.entity.mappers import DomainEntityConverter
from app.entity.relationships import reverse_relationships_for
from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.entity import Base
from bookstore.generated.schema import (
    RelationshipMetadata,
    SchemaClassAddressable,
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
        existing_entity = self._find_by_external_id(
            schema_class=schema_class,
            entity_id=entity_id,
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
        value: Identifier | list[Identifier] | DomainModel | list[DomainModel],
    ) -> object:
        target_schema_class = self._target_schema_class(
            relationship.target_class_name
        )
        values = value if isinstance(value, list) else [value]
        related_entities = [
            self._find_related_entity(
                name,
                target_schema_class,
                self._related_identifier(related_value),
            )
            for related_value in values
        ]
        return (
            related_entities
            if relationship.multivalued
            else related_entities[0]
        )

    @staticmethod
    def _related_identifier(value: Identifier | DomainModel) -> Identifier:
        return value.id if isinstance(value, DomainModel) else str(value)

    def _find_related_entity(
        self,
        relationship_name: str,
        target_schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> Base:
        entity = self._find_by_external_id(
            schema_class=target_schema_class,
            entity_id=str(entity_id),
        )
        if entity is None:
            raise RelatedEntityNotFound(relationship_name, str(entity_id))
        return entity

    def _find_by_external_id(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> Base | None:
        return self.session.execute(
            select(schema_class.entity_class).where(
                schema_class.entity_class.id == entity_id,
            )
        ).scalar_one_or_none()

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

    def _hydrate_reverse_relationships(
        self,
        schema_class: type[SchemaClassAddressable],
        model: DomainModel,
    ) -> DomainModel:
        for related_schema_class, forward_ref_name, reverse_field_name in (
            reverse_relationships_for(schema_class)
        ):
            related_models = self._find_all_without_hydration(related_schema_class)
            related_values = [
                related_model
                for related_model in related_models
                if self._matches_reference(related_model, forward_ref_name, model.id)
            ]
            if related_values:
                setattr(model, reverse_field_name, related_values)
        return model

    @staticmethod
    def _matches_reference(
        model: DomainModel, reference_field: str, target_id: str
    ) -> bool:
        value = getattr(model, reference_field, None)
        if value is None:
            return False
        # Handle single reference
        if hasattr(value, "id"):
            return value.id == target_id
        # Handle multivalued references
        if isinstance(value, list):
            return any(hasattr(item, "id") and item.id == target_id for item in value)
        return False

    def _find_all_without_hydration(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DomainModel]:
        entities = self.session.scalars(select(schema_class.entity_class)).all()
        return [
            self.converter.to_domain(schema_class, entity)
            for entity in entities
        ]

    def find_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DomainModel]:
        models = self._find_all_without_hydration(schema_class)
        return [
            self._hydrate_reverse_relationships(schema_class, model)
            for model in models
        ]

    def find_by_id(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> DomainModel | None:
        entity = self._find_by_external_id(
            schema_class=schema_class,
            entity_id=entity_id,
        )
        if entity is None:
            return None
        model = self.converter.to_domain(schema_class, entity)
        return self._hydrate_reverse_relationships(schema_class, model)
