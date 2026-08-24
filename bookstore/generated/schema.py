from dataclasses import dataclass
from typing import ClassVar, Optional, Type

from bookstore.generated.model import (
    Entity as EntityModel,
    Person as PersonModel,
    Book as BookModel,
    Author as AuthorModel,
    Publisher as PublisherModel,
    User as UserModel,
    Review as ReviewModel,
)

from bookstore.generated.entity import (
    Entity as EntityEntity,
    Person as PersonEntity,
    Book as BookEntity,
    Author as AuthorEntity,
    Publisher as PublisherEntity,
    User as UserEntity,
    Review as ReviewEntity,
)

@dataclass
class SchemaClass:
    model_class: ClassVar[Type]
    entity_class: ClassVar[Type]
    api_resource_name: ClassVar[Optional[str]]


@dataclass
class Entity(SchemaClass):
    model_class = EntityModel
    entity_class = EntityEntity
    api_resource_name = None

@dataclass
class Person(SchemaClass):
    model_class = PersonModel
    entity_class = PersonEntity
    api_resource_name = None

@dataclass
class Book(SchemaClass):
    model_class = BookModel
    entity_class = BookEntity
    api_resource_name = "books"

@dataclass
class Author(SchemaClass):
    model_class = AuthorModel
    entity_class = AuthorEntity
    api_resource_name = "authors"

@dataclass
class Publisher(SchemaClass):
    model_class = PublisherModel
    entity_class = PublisherEntity
    api_resource_name = None

@dataclass
class User(SchemaClass):
    model_class = UserModel
    entity_class = UserEntity
    api_resource_name = None

@dataclass
class Review(SchemaClass):
    model_class = ReviewModel
    entity_class = ReviewEntity
    api_resource_name = "reviews"
