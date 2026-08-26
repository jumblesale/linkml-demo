from bookstore.generated.dto import DTOCreate
from bookstore.generated.schema import SchemaClass
from app.entity.repository import EntityRepository


class EntityService:
    def __init__(
        self,
        repository: EntityRepository,
    ):
        self.repository = repository

    def create(
        self,
        schema_class: type[SchemaClass],
        payload: DTOCreate,
    ):
        ...
