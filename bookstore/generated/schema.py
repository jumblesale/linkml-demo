from dataclasses import dataclass
from typing import ClassVar, Optional, Type

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
class SchemaClass:
    model_class: ClassVar[Type]
    entity_class: ClassVar[Type]
    write_model: ClassVar[Optional[Type[DTOCreate]]]
    read_model: ClassVar[Optional[Type[DTORead]]]
    api_resource_name: ClassVar[Optional[str]]


@dataclass
class Model(SchemaClass):
    model_class = ModelModel
    entity_class = ModelEntity
    write_model = None
    read_model = None
    api_resource_name = None

@dataclass
class Person(SchemaClass):
    model_class = PersonModel
    entity_class = PersonEntity
    write_model = None
    read_model = None
    api_resource_name = None

@dataclass
class Book(SchemaClass):
    model_class = BookModel
    entity_class = BookEntity
    write_model = BookCreate
    read_model = BookRead
    api_resource_name = "books"

@dataclass
class Author(SchemaClass):
    model_class = AuthorModel
    entity_class = AuthorEntity
    write_model = AuthorCreate
    read_model = AuthorRead
    api_resource_name = "authors"

@dataclass
class Publisher(SchemaClass):
    model_class = PublisherModel
    entity_class = PublisherEntity
    write_model = PublisherCreate
    read_model = PublisherRead
    api_resource_name = "publishers"

@dataclass
class User(SchemaClass):
    model_class = UserModel
    entity_class = UserEntity
    write_model = UserCreate
    read_model = UserRead
    api_resource_name = "users"

@dataclass
class Review(SchemaClass):
    model_class = ReviewModel
    entity_class = ReviewEntity
    write_model = ReviewCreate
    read_model = ReviewRead
    api_resource_name = "reviews"
