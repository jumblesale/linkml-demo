from collections.abc import Collection
from dataclasses import fields, is_dataclass
from datetime import datetime
from typing import Any, TypeVar, cast, get_args, get_type_hints

from linkml_runtime.utils.metamodelcore import XSDDateTime

from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.entity import Base
from bookstore.generated.schema import SchemaClassAddressable

Target = TypeVar("Target")


def _entity_value(value: Any, source_type: Any) -> Any:
    if isinstance(value, list):
        return [_entity_value(item, source_type) for item in value]
    if isinstance(value, str) and (
        _contains_type(source_type, XSDDateTime)
    ):
        return datetime.fromisoformat(str(value))
    if (text := getattr(value, "text", None)) is not None:
        return text
    if (code := getattr(value, "code", None)) is not None:
        return _entity_value(code, source_type)
    return value


def _contains_type(annotation: Any, expected_type: type[Any]) -> bool:
    return annotation is expected_type or any(
        _contains_type(argument, expected_type)
        for argument in get_args(annotation)
    )


def map_fields(
    source: Any,
    target_class: type[Target],
    field_names: Collection[str] | None = None,
    **overrides: Any,
) -> Target:
    target_fields = (
        {field.name for field in fields(cast(Any, target_class))}
        if is_dataclass(target_class)
        else set(field_names or ())
    )
    source_fields = (
        fields(source)
        if is_dataclass(source)
        else fields(cast(Any, target_class))
    )
    source_field_types = (
        get_type_hints(type(source))
        if is_dataclass(source)
        else {}
    )
    values = {
        field.name: _entity_value(
            getattr(source, field.name),
            source_field_types.get(field.name),
        )
        for field in source_fields
        if field.name in target_fields
        and (field_names is None or field.name in field_names)
    }
    values.update(overrides)
    return target_class(**values)


class DtoDomainConverter:
    def to_domain(
        self,
        schema_class: type[SchemaClassAddressable],
        payload: DTOCreate,
        entity_id: str,
        created_at: datetime | None = None,
    ) -> DomainModel:
        return map_fields(
            source=payload,
            target_class=schema_class.model_class,
            id=entity_id,
            created_at=created_at,
        )

    def to_dto(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
    ) -> DTORead:
        return map_fields(
            source=domain,
            target_class=schema_class.read_model,
        )


class DomainEntityConverter:
    @staticmethod
    def _orm_relationship_names(
        schema_class: type[SchemaClassAddressable],
    ) -> set[str]:
        return set(schema_class.entity_class.__mapper__.relationships.keys())

    def to_entity(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
        relationship_values: dict[str, Any] | None = None,
    ) -> Base:
        relationship_names = (
            set(schema_class.relationships)
            & self._orm_relationship_names(schema_class)
        )
        entity = map_fields(
            source=domain,
            target_class=schema_class.entity_class,
            field_names=schema_class.entity_field_names() - relationship_names,
        )
        for name in relationship_names:
            if relationship_values is None or name not in relationship_values:
                continue
            setattr(entity, name, relationship_values[name])
        return entity

    def to_domain(
        self,
        schema_class: type[SchemaClassAddressable],
        entity: Base,
    ) -> DomainModel:
        relationship_names = (
            set(schema_class.relationships)
            & self._orm_relationship_names(schema_class)
        )
        overrides = {}
        for name, relationship in schema_class.relationships.items():
            if name not in relationship_names:
                continue
            value = getattr(entity, name, None)
            if value is None:
                continue
            values = value if relationship.multivalued else [value]
            ids = [related_entity.id for related_entity in values]
            overrides[name] = ids if relationship.multivalued else ids[0]
        return map_fields(
            source=entity,
            target_class=schema_class.model_class,
            field_names=schema_class.entity_field_names() - relationship_names,
            **overrides,
        )
