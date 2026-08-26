from app.entity.id import IdGenerator, Identifier
from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.schema import SchemaClassAddressable
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository


class EntityService:
    def __init__(
        self,
        repository: EntityRepository,
        converter: DtoDomainConverter,
        id_generator: IdGenerator,
    ):
        self.repository = repository
        self.converter = converter
        self.id_generator = id_generator

    def create(
        self,
        schema_class: type[SchemaClassAddressable],
        payload: DTOCreate,
    ) -> Identifier:
        domain = self.converter.to_domain(
            schema_class=schema_class,
            payload=payload,
            entity_id=(id := self.id_generator()),
        )
        self.repository.save(schema_class, domain)
        return id

    def get(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> DTORead | None:
        if (domain := self.repository.find_by_id(schema_class, entity_id)) is None:
            return None
        return self.converter.to_dto(schema_class, domain)

    def get_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DTORead]:
        return [
            self.converter.to_dto(schema_class, domain)
            for domain in self.repository.find_all(schema_class)
        ]
