import argparse
from collections.abc import Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.entity.repository import EntityRepository
from bookstore.generated.constraints import apply_constraints
from bookstore.generated.entity import Base

DATABASE_URL = "postgresql+psycopg://admin:password@localhost:5432/bookstore"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()


def entity_repository(
    session: Session = Depends(get_session),
) -> EntityRepository:
    return EntityRepository(session=session)


def clear_database() -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("DROP SCHEMA public CASCADE")
        connection.exec_driver_sql("CREATE SCHEMA public")
    apply_constraints()
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the bookstore database.")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete all database tables and recreate the schema.",
    )
    arguments = parser.parse_args()
    if arguments.clear:
        clear_database()
