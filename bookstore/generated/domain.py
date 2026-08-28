# Auto generated from bookstore.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-08-28T10:20:25
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

from linkml_runtime.linkml_model.types import Date, Datetime, String
from linkml_runtime.utils.metamodelcore import XSDDate, XSDDateTime

metamodel_version = "1.11.0"
version = None

# Namespaces
BOOKSTORE = CurieNamespace('bookstore', 'https://example.org/bookstore/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = BOOKSTORE


# Types

# Class references



@dataclass(repr=False)
class Model(YAMLRoot):
    """
    The base model for this project.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BOOKSTORE["Model"]
    class_class_curie: ClassVar[str] = "bookstore:Model"
    class_name: ClassVar[str] = "Model"
    class_model_uri: ClassVar[URIRef] = BOOKSTORE.Model

    id: str = None
    created_at: Union[str, XSDDateTime] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        if self._is_empty(self.created_at):
            self.MissingRequiredField("created_at")
        if not isinstance(self.created_at, XSDDateTime):
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

    id: str = None
    created_at: Union[str, XSDDateTime] = None
    name: str = None
    gender: Optional[str] = None
    date_of_birth: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
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

    id: str = None
    created_at: Union[str, XSDDateTime] = None
    title: str = None
    ISBN: str = None
    authors: Union[Union[dict, "Author"], list[Union[dict, "Author"]]] = None
    genre: Union[str, "Genre"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.ISBN):
            self.MissingRequiredField("ISBN")
        if not isinstance(self.ISBN, str):
            self.ISBN = str(self.ISBN)

        if self._is_empty(self.authors):
            self.MissingRequiredField("authors")
        self._normalize_inlined_as_list(slot_name="authors", slot_type=Author, key_name="id", keyed=False)

        if self._is_empty(self.genre):
            self.MissingRequiredField("genre")
        if not isinstance(self.genre, Genre):
            self.genre = Genre(self.genre)

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

    id: str = None
    created_at: Union[str, XSDDateTime] = None
    name: str = None
    books_published: Optional[Union[Union[dict, Book], list[Union[dict, Book]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="books_published", slot_type=Book, key_name="id", keyed=False)

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

    id: str = None
    created_at: Union[str, XSDDateTime] = None
    name: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
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

    id: str = None
    created_at: Union[str, XSDDateTime] = None
    name: str = None
    has_bought: Optional[Union[Union[dict, Book], list[Union[dict, Book]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="has_bought", slot_type=Book, key_name="id", keyed=False)

        super().__post_init__(**kwargs)


# Enumerations
class Genre(EnumDefinitionImpl):

    Fantasy = PermissibleValue(text="Fantasy")
    Crime = PermissibleValue(text="Crime")
    Thriller = PermissibleValue(text="Thriller")
    Biography = PermissibleValue(text="Biography")

    _defn = EnumDefinition(
        name="Genre",
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
                   model_uri=BOOKSTORE.id, domain=None, range=str)

slots.created_at = Slot(uri=BOOKSTORE.created_at, name="created_at", curie=BOOKSTORE.curie('created_at'),
                   model_uri=BOOKSTORE.created_at, domain=None, range=Union[str, XSDDateTime])

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
                   model_uri=BOOKSTORE.authors, domain=None, range=Union[Union[dict, Author], list[Union[dict, Author]]])

slots.genre = Slot(uri=BOOKSTORE.genre, name="genre", curie=BOOKSTORE.curie('genre'),
                   model_uri=BOOKSTORE.genre, domain=None, range=Union[str, "Genre"])

slots.books_published = Slot(uri=BOOKSTORE.books_published, name="books_published", curie=BOOKSTORE.curie('books_published'),
                   model_uri=BOOKSTORE.books_published, domain=None, range=Optional[Union[Union[dict, Book], list[Union[dict, Book]]]])

slots.has_bought = Slot(uri=BOOKSTORE.has_bought, name="has_bought", curie=BOOKSTORE.curie('has_bought'),
                   model_uri=BOOKSTORE.has_bought, domain=None, range=Optional[Union[Union[dict, Book], list[Union[dict, Book]]]])
