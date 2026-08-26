from collections.abc import Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.entity.repository import EntityRepository


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