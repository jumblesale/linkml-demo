from dataclasses import dataclass
from typing import ClassVar, Type

from bookstore.generated.domain import (
    Model as ModelModel,
    Person as PersonModel,
    Book as BookModel,
    User as UserModel,
)

from bookstore.generated.entity import (
    Model as ModelEntity,
    Person as PersonEntity,
    Book as BookEntity,
    User as UserEntity,
)

from bookstore.generated.dto import (
    DTOCreate,
    DTORead,
    BookRead,
    BookCreate,
    UserRead,
    UserCreate,
)

@dataclass(frozen=True)
class RelationshipMetadata:
    target_class_name: str
    multivalued: bool
    minimum_cardinality: int | None

@dataclass(frozen=True)
class RelationshipSchemaClass:
    model_class: ClassVar[Type]
    entity_class: ClassVar[Type]
    relationships: ClassVar[dict[str, RelationshipMetadata]]

    @classmethod
    def entity_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def entity_field_names(cls) -> set[str]:
        return set(cls.entity_class.__mapper__.attrs.keys())

@dataclass(frozen=True)
class SchemaClassAddressable(RelationshipSchemaClass):
    write_model: ClassVar[Type[DTOCreate]]
    read_model: ClassVar[Type[DTORead]]
    api_resource_name: ClassVar[str]


@dataclass(frozen=True)
class Model(RelationshipSchemaClass):
    model_class = ModelModel
    entity_class = ModelEntity
    relationships = {
    }

@dataclass(frozen=True)
class Person(RelationshipSchemaClass):
    model_class = PersonModel
    entity_class = PersonEntity
    relationships = {
    }

@dataclass(frozen=True)
class Book(SchemaClassAddressable):
    model_class = BookModel
    entity_class = BookEntity
    relationships = {
    }
    write_model = BookCreate
    read_model = BookRead
    api_resource_name = "books"

@dataclass(frozen=True)
class User(SchemaClassAddressable):
    model_class = UserModel
    entity_class = UserEntity
    relationships = {
        "has_bought": RelationshipMetadata(
            target_class_name="Book",
            multivalued=True,
            minimum_cardinality=0,
        ),
    }
    write_model = UserCreate
    read_model = UserRead
    api_resource_name = "users"
