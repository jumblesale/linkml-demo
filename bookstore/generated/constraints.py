from sqlalchemy import UniqueConstraint

from bookstore.generated.entity import (
    Book,
    User,
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
    User.__table__.append_constraint(
        UniqueConstraint(
            "email",
            name="uq_user_email",
        ),
    )