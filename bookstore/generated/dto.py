from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

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
    authors: list[str]
    genre: Literal['Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography']

@dataclass
class BookRead(DTORead):
    title: str
    ISBN: str
    authors: list[str]
    genre: Literal['Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography']
    id: str
    created_at: datetime | None


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
    created_at: datetime | None


@dataclass
class PublisherCreate(DTOCreate):
    name: str

@dataclass
class PublisherRead(DTORead):
    name: str
    id: str
    created_at: datetime | None


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
    created_at: datetime | None


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
    created_at: datetime | None
