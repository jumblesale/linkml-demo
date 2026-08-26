from dataclasses import dataclass
from typing import ClassVar, Type

from bookstore.generated.domain import (
    Model as ModelModel,
    Person as PersonModel,
    Book as BookModel,
    Author as AuthorModel,
    Publisher as PublisherModel,
    User as UserModel,
    Review as ReviewModel,
)

from bookstore.generated.entity import (
    Model as ModelEntity,
    Person as PersonEntity,
    Book as BookEntity,
    Author as AuthorEntity,
    Publisher as PublisherEntity,
    User as UserEntity,
    Review as ReviewEntity,
)

from bookstore.generated.dto import (
    DTOCreate,
    DTORead,
    BookRead,
    BookCreate,
    AuthorRead,
    AuthorCreate,
    PublisherRead,
    PublisherCreate,
    UserRead,
    UserCreate,
    ReviewRead,
    ReviewCreate,
)

@dataclass
class RelationshipSchemaClass:
    model_class: ClassVar[Type]
    entity_class: ClassVar[Type]

    @classmethod
    def entity_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def entity_field_names(cls) -> set[str]:
        return set(cls.entity_class.__mapper__.attrs.keys())

@dataclass
class SchemaClassAddressable(RelationshipSchemaClass):
    write_model: ClassVar[Type[DTOCreate]]
    read_model: ClassVar[Type[DTORead]]
    api_resource_name: ClassVar[str]


@dataclass
class Model(RelationshipSchemaClass):
    model_class = ModelModel
    entity_class = ModelEntity

@dataclass
class Person(RelationshipSchemaClass):
    model_class = PersonModel
    entity_class = PersonEntity

@dataclass
class Book(SchemaClassAddressable):
    model_class = BookModel
    entity_class = BookEntity
    write_model = BookCreate
    read_model = BookRead
    api_resource_name = "books"

@dataclass
class Author(SchemaClassAddressable):
    model_class = AuthorModel
    entity_class = AuthorEntity
    write_model = AuthorCreate
    read_model = AuthorRead
    api_resource_name = "authors"

@dataclass
class Publisher(SchemaClassAddressable):
    model_class = PublisherModel
    entity_class = PublisherEntity
    write_model = PublisherCreate
    read_model = PublisherRead
    api_resource_name = "publishers"

@dataclass
class User(SchemaClassAddressable):
    model_class = UserModel
    entity_class = UserEntity
    write_model = UserCreate
    read_model = UserRead
    api_resource_name = "users"

@dataclass
class Review(SchemaClassAddressable):
    model_class = ReviewModel
    entity_class = ReviewEntity
    write_model = ReviewCreate
    read_model = ReviewRead
    api_resource_name = "reviews"
