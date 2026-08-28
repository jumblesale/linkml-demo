from sqlalchemy import UniqueConstraint

from bookstore.generated.entity import (
    Book,
    Publisher,
)


def apply_constraints() -> None:
    Book.__table__.append_constraint(
        UniqueConstraint(
            "title",
            name="uq_book_title",
        ),
    )
    Book.__table__.append_constraint(
        UniqueConstraint(
            "ISBN",
            name="uq_book_isbn",
        ),
    )
    Publisher.__table__.append_constraint(
        UniqueConstraint(
            "name",
            name="uq_publisher_name",
        ),
    )