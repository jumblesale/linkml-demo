from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

@dataclass(frozen=True)
class DTO: ...

@dataclass(frozen=True)
class DTOCreate(DTO): ...

@dataclass(frozen=True)
class DTORead(DTO): ...


@dataclass(frozen=True)
class BookCreate(DTOCreate):
    title: str
    ISBN: str
    authors: list[str]
    genre: Literal['Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography']

@dataclass(frozen=True)
class BookRead(DTORead):
    title: str
    ISBN: str
    authors: list[str]
    genre: Literal['Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography']
    id: str
    created_at: datetime | None = None


@dataclass(frozen=True)
class AuthorCreate(DTOCreate):
    name: str
    gender: str | None = None
    date_of_birth: date | None = None

@dataclass(frozen=True)
class AuthorRead(DTORead):
    name: str
    id: str
    gender: str | None = None
    date_of_birth: date | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class PublisherCreate(DTOCreate):
    name: str

@dataclass(frozen=True)
class PublisherRead(DTORead):
    name: str
    id: str
    created_at: datetime | None = None


@dataclass(frozen=True)
class UserCreate(DTOCreate):
    name: str
    gender: str | None = None
    date_of_birth: date | None = None

@dataclass(frozen=True)
class UserRead(DTORead):
    name: str
    id: str
    gender: str | None = None
    date_of_birth: date | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class ReviewCreate(DTOCreate):
    user: str
    score: int
    review_text: str | None = None

@dataclass(frozen=True)
class ReviewRead(DTORead):
    score: int
    id: str
    review_text: str | None = None
    created_at: datetime | None = None
