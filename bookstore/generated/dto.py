from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class DTO: ...

@dataclass
class DTOCreate(DTO): ...

@dataclass
class DTORead(DTO): ...


class BookCreate(DTOCreate):
    title: str
    ISBN: str
    genre: str

class BookRead(DTORead):
    title: str
    ISBN: str
    genre: str
    id: str


class AuthorCreate(DTOCreate):
    name: str
    gender: str | None
    date_of_birth: date | None

class AuthorRead(DTORead):
    name: str
    gender: str | None
    date_of_birth: date | None
    id: str


class PublisherCreate(DTOCreate):
    name: str

class PublisherRead(DTORead):
    name: str
    id: str


class UserCreate(DTOCreate):
    name: str
    gender: str | None
    date_of_birth: date | None

class UserRead(DTORead):
    name: str
    gender: str | None
    date_of_birth: date | None
    id: str


class ReviewCreate(DTOCreate):
    user: str
    score: int
    review_text: str | None

class ReviewRead(DTORead):
    score: int
    review_text: str | None
    id: str
