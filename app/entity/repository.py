from sqlalchemy import UniqueConstraint, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Table
from typing import cast

from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.entity import Base
from bookstore.generated.schema import SchemaClassAddressable
from app.entity.mappers import DomainEntityConverter
from app.entity.exceptions import UniqueConstraintViolation


class EntityRepository:
    def __init__(self, session: Session):
        self.converter = DomainEntityConverter()
        self.session = session

    def save(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
    ) -> None:
        entity = self.converter.to_entity(schema_class, domain)
        try:
            self.session.add(entity)
            self.session.flush()
        except IntegrityError as error:
            if not self._is_unique_violation(error):
                raise
            field = self._unique_field(entity, error)
            raise UniqueConstraintViolation(field) from error

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
        entity_id: str,
    ) -> DomainModel | None:
        entity = self.session.get(schema_class.entity_class, entity_id)
        if entity is None:
            return None
        return self.converter.to_domain(schema_class, entity)
