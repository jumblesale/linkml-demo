from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    Time,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


metadata = Base.metadata


class Model(Base):
    """
    The base model for this project.
    """

    __tablename__ = "Model"

    uid: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return f"Model(uid={self.uid},id={self.id},created_at={self.created_at},)"


class BookAuthors(Base):
    """
    None
    """

    __tablename__ = "Book_authors"

    Book_uid: Mapped[int] = mapped_column(Integer(), ForeignKey("Book.uid"), primary_key=True)
    authors_uid: Mapped[int] = mapped_column(Integer(), ForeignKey("Author.uid"), primary_key=True)

    def __repr__(self):
        return f"Book_authors(Book_uid={self.Book_uid},authors_uid={self.authors_uid},)"


class AuthorBooksPublished(Base):
    """
    None
    """

    __tablename__ = "Author_books_published"

    Author_uid: Mapped[int] = mapped_column(Integer(), ForeignKey("Author.uid"), primary_key=True)
    books_published_uid: Mapped[int] = mapped_column(Integer(), ForeignKey("Book.uid"), primary_key=True)

    def __repr__(self):
        return f"Author_books_published(Author_uid={self.Author_uid},books_published_uid={self.books_published_uid},)"


class UserHasBought(Base):
    """
    None
    """

    __tablename__ = "User_has_bought"

    User_uid: Mapped[int] = mapped_column(Integer(), ForeignKey("User.uid"), primary_key=True)
    has_bought_uid: Mapped[int] = mapped_column(Integer(), ForeignKey("Book.uid"), primary_key=True)

    def __repr__(self):
        return f"User_has_bought(User_uid={self.User_uid},has_bought_uid={self.has_bought_uid},)"


class Person(Model):
    """
    The base class of a human being.
    """

    __tablename__ = "Person"

    uid: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(Text())
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    id: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return f"Person(uid={self.uid},name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Book(Model):
    """
    A book sold by the bookstore.
    """

    __tablename__ = "Book"

    uid: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text())
    ISBN: Mapped[str] = mapped_column(Text())
    genre: Mapped[str] = mapped_column(Enum('Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography', name='Genre'))
    id: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    # ManyToMany
    authors: Mapped[list[Author]] = relationship(secondary="Book_authors")

    def __repr__(self):
        return f"Book(uid={self.uid},title={self.title},ISBN={self.ISBN},genre={self.genre},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Publisher(Model):
    """
    An organization who publishes books sold by the bookstore.
    """

    __tablename__ = "Publisher"

    uid: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    id: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return f"Publisher(uid={self.uid},name={self.name},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Author(Person):
    """
    A human who has authored books sold by the bookstore.
    """

    __tablename__ = "Author"

    uid: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(Text())
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    id: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    # ManyToMany
    books_published: Mapped[list[Book]] = relationship(secondary="Author_books_published")

    def __repr__(self):
        return f"Author(uid={self.uid},name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class User(Person):
    """
    A customer of the bookstore.
    """

    __tablename__ = "User"

    uid: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(Text())
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    id: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())

    # ManyToMany
    has_bought: Mapped[list[Book]] = relationship(secondary="User_has_bought")

    def __repr__(self):
        return f"User(uid={self.uid},name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}
