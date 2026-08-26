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
    The base model for any addressable entity in the bookstore.
    """

    __tablename__ = "Model"

    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    def __repr__(self):
        return f"Model(id={self.id},created_at={self.created_at},)"


class BookAuthors(Base):
    """
    None
    """

    __tablename__ = "Book_authors"

    Book_id: Mapped[str] = mapped_column(Text(), ForeignKey("Book.id"), primary_key=True)
    authors_id: Mapped[str] = mapped_column(Text(), ForeignKey("Author.id"), primary_key=True)

    def __repr__(self):
        return f"Book_authors(Book_id={self.Book_id},authors_id={self.authors_id},)"


class BookReviews(Base):
    """
    None
    """

    __tablename__ = "Book_reviews"

    Book_id: Mapped[str] = mapped_column(Text(), ForeignKey("Book.id"), primary_key=True)
    reviews_id: Mapped[str] = mapped_column(Text(), ForeignKey("Review.id"), primary_key=True)

    def __repr__(self):
        return f"Book_reviews(Book_id={self.Book_id},reviews_id={self.reviews_id},)"


class AuthorBooksPublished(Base):
    """
    None
    """

    __tablename__ = "Author_books_published"

    Author_id: Mapped[str] = mapped_column(Text(), ForeignKey("Author.id"), primary_key=True)
    books_published_id: Mapped[str] = mapped_column(Text(), ForeignKey("Book.id"), primary_key=True)

    def __repr__(self):
        return f"Author_books_published(Author_id={self.Author_id},books_published_id={self.books_published_id},)"


class UserHasBought(Base):
    """
    None
    """

    __tablename__ = "User_has_bought"

    User_id: Mapped[str] = mapped_column(Text(), ForeignKey("User.id"), primary_key=True)
    has_bought_id: Mapped[str] = mapped_column(Text(), ForeignKey("Book.id"), primary_key=True)

    def __repr__(self):
        return f"User_has_bought(User_id={self.User_id},has_bought_id={self.has_bought_id},)"


class UserReviews(Base):
    """
    None
    """

    __tablename__ = "User_reviews"

    User_id: Mapped[str] = mapped_column(Text(), ForeignKey("User.id"), primary_key=True)
    reviews_id: Mapped[str] = mapped_column(Text(), ForeignKey("Review.id"), primary_key=True)

    def __repr__(self):
        return f"User_reviews(User_id={self.User_id},reviews_id={self.reviews_id},)"


class Person(Model):
    """
    The base class of a human being.
    """

    __tablename__ = "Person"

    name: Mapped[str] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(Text())
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    def __repr__(self):
        return f"Person(name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Book(Model):
    """
    A book sold by the bookstore.
    """

    __tablename__ = "Book"

    title: Mapped[str] = mapped_column(Text())
    ISBN: Mapped[str] = mapped_column(Text())
    publisher: Mapped[str | None] = mapped_column(Text(), ForeignKey("Publisher.id"))
    genre: Mapped[str] = mapped_column(Enum('Sci-fi', 'Fantasy', 'Crime', 'Thriller', 'Non-fiction', 'Biography', name='Genre'))
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    # ManyToMany
    authors: Mapped[list[Author]] = relationship(secondary="Book_authors")

    # ManyToMany
    reviews: Mapped[list[Review]] = relationship(secondary="Book_reviews")

    def __repr__(self):
        return f"Book(title={self.title},ISBN={self.ISBN},publisher={self.publisher},genre={self.genre},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Publisher(Model):
    """
    An organization who publishes books sold by the bookstore.
    """

    __tablename__ = "Publisher"

    name: Mapped[str] = mapped_column(Text())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    def __repr__(self):
        return f"Publisher(name={self.name},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Review(Model):
    """
    A user-submitted review of a book in the store.
    """

    __tablename__ = "Review"

    user: Mapped[str] = mapped_column(Text(), ForeignKey("User.id"))
    score: Mapped[int] = mapped_column(Integer())
    review_text: Mapped[str | None] = mapped_column(Text())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    def __repr__(self):
        return f"Review(user={self.user},score={self.score},review_text={self.review_text},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class Author(Person):
    """
    A human who has authored books sold by the bookstore.
    """

    __tablename__ = "Author"

    name: Mapped[str] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(Text())
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    # ManyToMany
    books_published: Mapped[list[Book]] = relationship(secondary="Author_books_published")

    def __repr__(self):
        return f"Author(name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}


class User(Person):
    """
    A customer of the bookstore.
    """

    __tablename__ = "User"

    name: Mapped[str] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(Text())
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    id: Mapped[str] = mapped_column(Text(), primary_key=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime())

    # ManyToMany
    has_bought: Mapped[list[Book]] = relationship(secondary="User_has_bought")

    # ManyToMany
    reviews: Mapped[list[Review]] = relationship(secondary="User_reviews")

    def __repr__(self):
        return f"User(name={self.name},gender={self.gender},date_of_birth={self.date_of_birth},id={self.id},created_at={self.created_at},)"

    __mapper_args__ = {"concrete": True}
