from collections.abc import Collection
from dataclasses import fields, is_dataclass
from typing import Any, TypeVar, cast

from bookstore.generated.domain import Model as DomainModel
from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.entity import Base
from bookstore.generated.schema import SchemaClassAddressable


Target = TypeVar("Target")


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
    values = {
        field.name: getattr(source, field.name)
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
    ) -> DomainModel:
        return map_fields(
            source=payload,
            target_class=schema_class.model_class,
            id=entity_id,
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
    def to_entity(
        self,
        schema_class: type[SchemaClassAddressable],
        domain: DomainModel,
    ) -> Base:
        entity_fields = schema_class.entity_class.__mapper__.attrs.keys()
        return map_fields(
            source=domain,
            target_class=schema_class.entity_class,
            field_names=entity_fields,
        )

    def to_domain(
        self,
        schema_class: type[SchemaClassAddressable],
        entity: Base,
    ) -> DomainModel:
        entity_fields = schema_class.entity_class.__mapper__.attrs.keys()
        return map_fields(
            source=entity,
            target_class=schema_class.model_class,
            field_names=entity_fields,
        )