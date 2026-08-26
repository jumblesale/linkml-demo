from app.entity.id import IdGenerator, Identifier
from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.schema import SchemaClassAddressable
from app.entity.converter import EntityConverter
from app.entity.repository import EntityRepository


class EntityService:
    def __init__(
        self,
        repository: EntityRepository,
        converter: EntityConverter,
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
        entity = self.converter.to_entity(
            schema_class=schema_class,
            payload=payload,
            entity_id=(id := self.id_generator()),
        )
        self.repository.save(entity)
        return id

    def get(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> DTORead | None:
        if (entity := self.repository.find_by_id(entity_id)) is None:
            return None
        return self.converter.to_read_model(schema_class, entity)

    def get_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DTORead]:
        return [
            self.converter.to_read_model(schema_class, entity)
            for entity in self.repository.find_all()
            if isinstance(entity, schema_class.entity_class)
        ]
