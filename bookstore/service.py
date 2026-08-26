from bookstore.generated.model import Model
from bookstore.generated.schema import SchemaClass
from bookstore.repository import Repository


class EntityService:
    def __init__(
        self,
        repository: Repository,
    ):
        self.repository = repository

    def create(
        self,
        schema_class: type[SchemaClass],
        model: Model,
    ):
        ...
