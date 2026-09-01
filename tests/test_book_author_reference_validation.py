import pytest
from fastapi.testclient import TestClient

from app.app import fast_api
from app.database import clear_database, SessionLocal
from app.entity.exceptions import RelatedEntityNotFound
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository
from app.entity.service import EntityService
from app.entity.validator import ModelValidator
from app.entity.id import id_generator
from bookstore.generated.dto import AuthorCreate, BookCreate
from bookstore.generated.schema import Author, Book


@pytest.fixture
def service():
    clear_database()
    session = SessionLocal()
    try:
        yield EntityService(
            repository=EntityRepository(session=session),
            converter=DtoDomainConverter(),
            id_generator=id_generator,
            validator=ModelValidator(),
        )
    finally:
        session.close()


def test_creating_book_with_unknown_author_id_raises_related_entity_not_found(service):
    with pytest.raises(RelatedEntityNotFound):
        service.create(
            schema_class=Book,
            payload=BookCreate(
                title="Dune",
                ISBN="1234567890123",
                author="author-does-not-exist",
                genre="Sci-fi",
            ),
        )


def test_creating_book_with_existing_author_id_succeeds(service):
    author_id = service.create(
        schema_class=Author,
        payload=AuthorCreate(name="Frank Herbert"),
    )

    book_id = service.create(
        schema_class=Book,
        payload=BookCreate(
            title="Dune",
            ISBN="1234567890123",
            author=author_id,
            genre="Sci-fi",
        ),
    )

    assert book_id


def test_api_can_create_book_with_author_id_from_previous_author_create():
    clear_database()
    client = TestClient(fast_api)

    author_response = client.post(
        "/authors",
        json={"name": "Frank Herbert"},
    )
    assert author_response.status_code == 201

    author_id = author_response.headers["Location"].rsplit("/", 1)[-1]

    book_response = client.post(
        "/books",
        json={
            "title": "Dune",
            "ISBN": "1234567890123",
            "author": author_id,
            "genre": "Sci-fi",
        },
    )

    assert book_response.status_code == 201

    book_id = book_response.headers["Location"].rsplit("/", 1)[-1]
    author_read_response = client.get(f"/authors/{author_id}")

    assert author_read_response.status_code == 200
    assert author_read_response.json()["books_published"] == [book_id]
