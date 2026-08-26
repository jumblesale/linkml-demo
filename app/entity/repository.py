from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.schema import SchemaClassAddressable
from app.entity.mappers import DomainEntityConverter


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
