from sqlalchemy import UniqueConstraint

from bookstore.generated.entity import (
    Book,
)


def apply_constraints() -> None:
    Book.__table__.append_constraint(
        UniqueConstraint(
            "title",
            name="uq_book_unique_title",
        ),
    )
    Book.__table__.append_constraint(
        UniqueConstraint(
            "ISBN",
            name="uq_book_unique_isbn",
        ),
    )