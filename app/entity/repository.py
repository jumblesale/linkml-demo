from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.entity import Base
from bookstore.generated.schema import SchemaClassAddressable
from app.entity.mappers import DomainEntityConverter


class EntityRepository:
    def __init__(self, session: Session | None = None):
        self.converter = DomainEntityConverter()
        self.session = session
        self.entities: list[Base] = []

    def save(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
    ) -> None:
        entity = self.converter.to_entity(schema_class, domain)
        if self.session is None:
            self.entities.append(entity)
            return

        self.session.add(entity)
        self.session.flush()

    @staticmethod
    def _is_unique_violation(error: IntegrityError) -> bool:
        message = str(error.orig).lower()
        return "unique constraint" in message or "duplicate key" in message

    def find_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DomainModel]:
        return [
            self.converter.to_domain(schema_class, entity)
            for entity in self.entities
            if isinstance(entity, schema_class.entity_class)
        ]

    def find_by_id(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: str,
    ) -> DomainModel | None:
        entity = next(
            (
                entity
                for entity in self.entities
                if isinstance(entity, schema_class.entity_class)
                and getattr(entity, "id", None) == entity_id
            ),
            None,
        )
        if entity is None:
            return None
        return self.converter.to_domain(schema_class, entity)
