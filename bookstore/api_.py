from __future__ import annotations

import os
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Iterator
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from bookstore.generated.entity import Base
from bookstore.generated.schema import SchemaClass


DATABASE_URL = os.getenv("BOOKSTORE_DATABASE_URL", "sqlite:///./bookstore.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

app = FastAPI(title="Bookstore API")


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def _schema_classes() -> list[type[SchemaClass]]:
    return [schema_class for schema_class in SchemaClass.__subclasses__() if schema_class.api_resource_name]


def _normalise(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_normalise(item) for item in value]
    return value


def _serialise(entity: Any) -> dict[str, Any]:
    mapper = inspect(entity).mapper
    result = {
        column.key: _normalise(getattr(entity, column.key))
        for column in mapper.columns
    }
    for relationship in mapper.relationships:
        related = getattr(entity, relationship.key)
        if relationship.uselist:
            result[relationship.key] = [item.id for item in related]
        else:
            result[relationship.key] = related.id if related is not None else None
    return result


def _relationship_ids(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _entity_class_for_table(table_name: str) -> type[Any] | None:
    for schema_class in _schema_classes():
        if schema_class.entity_class.__tablename__ == table_name:
            return schema_class.entity_class
    return None


def _create_handler(schema_class: type[SchemaClass]):
    model_class = schema_class.model_class
    entity_class = schema_class.entity_class
    model_fields = set(model_class.__dataclass_fields__)
    mapper = inspect(entity_class)
    column_names = {column.key for column in mapper.columns}
    relationship_by_name = {relationship.key: relationship for relationship in mapper.relationships}

    def create(payload: dict[str, Any], session: Session = Depends(get_session)) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise HTTPException(status_code=422, detail="Request body must be a JSON object")

        infrastructure_fields = {"id", "created_at"}
        unknown_fields = set(payload) - model_fields
        read_only_fields = (set(payload) & infrastructure_fields) | ({"average_rating"} & set(payload))
        if unknown_fields or read_only_fields:
            invalid_fields = sorted(unknown_fields | read_only_fields)
            raise HTTPException(status_code=422, detail=f"Invalid fields: {', '.join(invalid_fields)}")

        values = dict(payload)
        values["id"] = str(uuid4())
        values["created_at"] = datetime.now(timezone.utc)
        try:
            model = model_class(**values)
        except (TypeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

        entity_values = {
            name: getattr(model, name)
            for name in column_names
            if name in model_fields and hasattr(model, name)
        }
        entity_values["id"] = values["id"]
        entity_values["created_at"] = values["created_at"]
        entity = entity_class(**entity_values)

        for column in mapper.columns:
            if not column.foreign_keys or entity_values.get(column.key) is None:
                continue
            foreign_key = next(iter(column.foreign_keys))
            related_class = _entity_class_for_table(foreign_key.column.table.name)
            if related_class is not None and session.get(related_class, entity_values[column.key]) is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Referenced {related_class.__name__} '{entity_values[column.key]}' does not exist",
                )

        for name, relationship in relationship_by_name.items():
            if name not in payload:
                continue
            related_class = relationship.mapper.class_
            related_entities = []
            for related_id in _relationship_ids(getattr(model, name)):
                related_entity = session.get(related_class, related_id)
                if related_entity is None:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail=f"Referenced {related_class.__name__} '{related_id}' does not exist",
                    )
                related_entities.append(related_entity)
            setattr(entity, name, related_entities if relationship.uselist else related_entities[0])

        session.add(entity)
        try:
            session.commit()
        except IntegrityError as error:
            session.rollback()
            raise HTTPException(status_code=409, detail="Entity violates a database constraint") from error
        session.refresh(entity)
        return _serialise(entity)

    create.__name__ = f"create_{schema_class.api_resource_name}"
    return create


Base.metadata.create_all(engine)

for schema_class in _schema_classes():
    app.post(
        f"/{schema_class.api_resource_name}",
        name=f"create_{schema_class.api_resource_name}",
        status_code=status.HTTP_201_CREATED,
    )(_create_handler(schema_class))
