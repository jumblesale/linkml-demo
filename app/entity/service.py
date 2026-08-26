from datetime import datetime, timezone

from app.entity.id import IdGenerator, Identifier
from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.schema import SchemaClassAddressable
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository
from app.entity.validator import ModelValidator


class EntityService:
    def __init__(
        self,
        repository: EntityRepository,
        converter: DtoDomainConverter,
        id_generator: IdGenerator,
        validator: ModelValidator,
    ):
        self.repository = repository
        self.converter = converter
        self.id_generator = id_generator
        self.validator = validator

    def create(
        self,
        schema_class: type[SchemaClassAddressable],
        payload: DTOCreate,
    ) -> Identifier:
        model = self.converter.to_domain(
            schema_class=schema_class,
            payload=payload,
            entity_id=(id := self.id_generator()),
            created_at=datetime.now(timezone.utc),
        )
        self.validator.validate(schema_class, model)
        self.repository.save(schema_class, model)
        return id

    def get(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> DTORead | None:
        if (model := self.repository.find_by_id(schema_class, entity_id)) is None:
            return None
        return self.converter.to_dto(schema_class, model)

    def get_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DTORead]:
        return [
            self.converter.to_dto(schema_class, model)
            for model in self.repository.find_all(schema_class)
        ]
