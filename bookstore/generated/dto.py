from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class DTO: ...

@dataclass
class DTOCreate(DTO): ...

@dataclass
class DTORead(DTO): ...


@dataclass
class BookCreate(DTOCreate):
    title: str
    ISBN: str
    genre: str

@dataclass
class BookRead(DTORead):
    title: str
    ISBN: str
    genre: str
    id: str


@dataclass
class AuthorCreate(DTOCreate):
    name: str
    gender: str | None
    date_of_birth: date | None

@dataclass
class AuthorRead(DTORead):
    name: str
    gender: str | None
    date_of_birth: date | None
    id: str


@dataclass
class PublisherCreate(DTOCreate):
    name: str

@dataclass
class PublisherRead(DTORead):
    name: str
    id: str


@dataclass
class UserCreate(DTOCreate):
    name: str
    gender: str | None
    date_of_birth: date | None

@dataclass
class UserRead(DTORead):
    name: str
    gender: str | None
    date_of_birth: date | None
    id: str


@dataclass
class ReviewCreate(DTOCreate):
    user: str
    score: int
    review_text: str | None

@dataclass
class ReviewRead(DTORead):
    score: int
    review_text: str | None
    id: str
