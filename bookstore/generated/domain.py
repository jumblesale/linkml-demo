# Auto generated from bookstore.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-08-26T10:14:32
# Schema: bookstore
#
# id: https://example.org/bookstore
# description: Schema for a fictional bookstore, including entities and their relationships.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Date, Datetime, Integer, String
from linkml_runtime.utils.metamodelcore import XSDDate, XSDDateTime

metamodel_version = "1.11.0"
version = None

# Namespaces
BOOKSTORE = CurieNamespace('bookstore', 'https://example.org/bookstore/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = BOOKSTORE


# Types

# Class references
class ModelId(extended_str):
    pass


class PersonId(ModelId):
    pass


class BookId(ModelId):
    pass


class AuthorId(PersonId):
    pass


class PublisherId(ModelId):
    pass


class UserId(PersonId):
    pass


class ReviewId(ModelId):
    pass


@dataclass(repr=False)
class Model(YAMLRoot):
    """
    The base model for any addressable entity in the bookstore.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Model"]
    class_class_curie: ClassVar[str] = "bookstore:Model"
    class_name: ClassVar[str] = "Model"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Model

    id: Union[str, ModelId] = None
    created_at: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ModelId):
            self.id = ModelId(self.id)

        if self.created_at is not None and not isinstance(self.created_at, XSDDateTime):
            self.created_at = XSDDateTime(self.created_at)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(Model):
    """
    The base class of a human being.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Person"]
    class_class_curie: ClassVar[str] = "bookstore:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Person

    id: Union[str, PersonId] = None
    name: str = None
    gender: Optional[str] = None
    date_of_birth: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.gender is not None and not isinstance(self.gender, str):
            self.gender = str(self.gender)

        if self.date_of_birth is not None and not isinstance(self.date_of_birth, XSDDate):
            self.date_of_birth = XSDDate(self.date_of_birth)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Book(Model):
    """
    A book sold by the bookstore.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Book"]
    class_class_curie: ClassVar[str] = "bookstore:Book"
    class_name: ClassVar[str] = "Book"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Book

    id: Union[str, BookId] = None
    title: str = None
    ISBN: str = None
    genre: Union[str, "Genre"] = None
    authors: Optional[Union[Union[str, AuthorId], list[Union[str, AuthorId]]]] = empty_list()
    publisher: Optional[Union[str, PublisherId]] = None
    reviews: Optional[Union[Union[str, ReviewId], list[Union[str, ReviewId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BookId):
            self.id = BookId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.ISBN):
            self.MissingRequiredField("ISBN")
        if not isinstance(self.ISBN, str):
            self.ISBN = str(self.ISBN)

        if self._is_empty(self.genre):
            self.MissingRequiredField("genre")
        if not isinstance(self.genre, Genre):
            self.genre = Genre(self.genre)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [v if isinstance(v, AuthorId) else AuthorId(v) for v in self.authors]

        if self.publisher is not None and not isinstance(self.publisher, PublisherId):
            self.publisher = PublisherId(self.publisher)

        if not isinstance(self.reviews, list):
            self.reviews = [self.reviews] if self.reviews is not None else []
        self.reviews = [v if isinstance(v, ReviewId) else ReviewId(v) for v in self.reviews]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Author(Person):
    """
    A human who has authored books sold by the bookstore.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Author"]
    class_class_curie: ClassVar[str] = "bookstore:Author"
    class_name: ClassVar[str] = "Author"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Author

    id: Union[str, AuthorId] = None
    name: str = None
    books_published: Optional[Union[Union[str, BookId], list[Union[str, BookId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AuthorId):
            self.id = AuthorId(self.id)

        if not isinstance(self.books_published, list):
            self.books_published = [self.books_published] if self.books_published is not None else []
        self.books_published = [v if isinstance(v, BookId) else BookId(v) for v in self.books_published]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Publisher(Model):
    """
    An organization who publishes books sold by the bookstore.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Publisher"]
    class_class_curie: ClassVar[str] = "bookstore:Publisher"
    class_name: ClassVar[str] = "Publisher"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Publisher

    id: Union[str, PublisherId] = None
    name: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PublisherId):
            self.id = PublisherId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class User(Person):
    """
    A customer of the bookstore.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["User"]
    class_class_curie: ClassVar[str] = "bookstore:User"
    class_name: ClassVar[str] = "User"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.User

    id: Union[str, UserId] = None
    name: str = None
    has_bought: Optional[Union[Union[str, BookId], list[Union[str, BookId]]]] = empty_list()
    reviews: Optional[Union[Union[str, ReviewId], list[Union[str, ReviewId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UserId):
            self.id = UserId(self.id)

        if not isinstance(self.has_bought, list):
            self.has_bought = [self.has_bought] if self.has_bought is not None else []
        self.has_bought = [v if isinstance(v, BookId) else BookId(v) for v in self.has_bought]

        if not isinstance(self.reviews, list):
            self.reviews = [self.reviews] if self.reviews is not None else []
        self.reviews = [v if isinstance(v, ReviewId) else ReviewId(v) for v in self.reviews]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Review(Model):
    """
    A user-submitted review of a book in the store.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Review"]
    class_class_curie: ClassVar[str] = "bookstore:Review"
    class_name: ClassVar[str] = "Review"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Review

    id: Union[str, ReviewId] = None
    user: Union[str, UserId] = None
    score: int = None
    review_text: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReviewId):
            self.id = ReviewId(self.id)

        if self._is_empty(self.user):
            self.MissingRequiredField("user")
        if not isinstance(self.user, UserId):
            self.user = UserId(self.user)

        if self._is_empty(self.score):
            self.MissingRequiredField("score")
        if not isinstance(self.score, int):
            self.score = int(self.score)

        if self.review_text is not None and not isinstance(self.review_text, str):
            self.review_text = str(self.review_text)

        super().__post_init__(**kwargs)


# Enumerations
class Genre(EnumDefinitionImpl):
    """
    The genre of a book.
    """
    Fantasy = PermissibleValue(text="Fantasy")
    Crime = PermissibleValue(text="Crime")
    Thriller = PermissibleValue(text="Thriller")
    Biography = PermissibleValue(text="Biography")

    _defn = EnumDefinition(
        name="Genre",
        description="The genre of a book.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Sci-fi",
            PermissibleValue(text="Sci-fi"))
        setattr(cls, "Non-fiction",
            PermissibleValue(text="Non-fiction"))

# Slots
class slots:
    pass

slots.id = Slot(uri=BOOKSTORE.id, name="id", curie=BOOKSTORE.curie('id'),
                   model_uri=BOOKSTORE.id, domain=None, range=URIRef)

slots.created_at = Slot(uri=BOOKSTORE.created_at, name="created_at", curie=BOOKSTORE.curie('created_at'),
                   model_uri=BOOKSTORE.created_at, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.name = Slot(uri=BOOKSTORE.name, name="name", curie=BOOKSTORE.curie('name'),
                   model_uri=BOOKSTORE.name, domain=None, range=str)

slots.gender = Slot(uri=BOOKSTORE.gender, name="gender", curie=BOOKSTORE.curie('gender'),
                   model_uri=BOOKSTORE.gender, domain=None, range=Optional[str])

slots.date_of_birth = Slot(uri=BOOKSTORE.date_of_birth, name="date_of_birth", curie=BOOKSTORE.curie('date_of_birth'),
                   model_uri=BOOKSTORE.date_of_birth, domain=None, range=Optional[Union[str, XSDDate]])

slots.title = Slot(uri=BOOKSTORE.title, name="title", curie=BOOKSTORE.curie('title'),
                   model_uri=BOOKSTORE.title, domain=None, range=str)

slots.ISBN = Slot(uri=BOOKSTORE.ISBN, name="ISBN", curie=BOOKSTORE.curie('ISBN'),
                   model_uri=BOOKSTORE.ISBN, domain=None, range=str,
                   pattern=re.compile(r'^[0-9]{13}$'))

slots.authors = Slot(uri=BOOKSTORE.authors, name="authors", curie=BOOKSTORE.curie('authors'),
                   model_uri=BOOKSTORE.authors, domain=None, range=Optional[Union[Union[str, AuthorId], list[Union[str, AuthorId]]]])

slots.publisher = Slot(uri=BOOKSTORE.publisher, name="publisher", curie=BOOKSTORE.curie('publisher'),
                   model_uri=BOOKSTORE.publisher, domain=None, range=Optional[Union[str, PublisherId]])

slots.genre = Slot(uri=BOOKSTORE.genre, name="genre", curie=BOOKSTORE.curie('genre'),
                   model_uri=BOOKSTORE.genre, domain=None, range=Union[str, "Genre"])

slots.reviews = Slot(uri=BOOKSTORE.reviews, name="reviews", curie=BOOKSTORE.curie('reviews'),
                   model_uri=BOOKSTORE.reviews, domain=None, range=Optional[Union[Union[str, ReviewId], list[Union[str, ReviewId]]]])

slots.books_published = Slot(uri=BOOKSTORE.books_published, name="books_published", curie=BOOKSTORE.curie('books_published'),
                   model_uri=BOOKSTORE.books_published, domain=None, range=Optional[Union[Union[str, BookId], list[Union[str, BookId]]]])

slots.has_bought = Slot(uri=BOOKSTORE.has_bought, name="has_bought", curie=BOOKSTORE.curie('has_bought'),
                   model_uri=BOOKSTORE.has_bought, domain=None, range=Optional[Union[Union[str, BookId], list[Union[str, BookId]]]])

slots.user = Slot(uri=BOOKSTORE.user, name="user", curie=BOOKSTORE.curie('user'),
                   model_uri=BOOKSTORE.user, domain=None, range=Union[str, UserId])

slots.score = Slot(uri=BOOKSTORE.score, name="score", curie=BOOKSTORE.curie('score'),
                   model_uri=BOOKSTORE.score, domain=None, range=int)

slots.review_text = Slot(uri=BOOKSTORE.review_text, name="review_text", curie=BOOKSTORE.curie('review_text'),
                   model_uri=BOOKSTORE.review_text, domain=None, range=Optional[str])
