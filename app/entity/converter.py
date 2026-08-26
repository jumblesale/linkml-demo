from dataclasses import fields

from bookstore.generated.dto import DTOCreate
from bookstore.generated.schema import SchemaClass


class EntityConverter:
    def to_entity(
        self,
        schema_class: type[SchemaClass],
        payload: DTOCreate,
        entity_id: str,
    ):
        values = {
            field.name: getattr(payload, field.name)
            for field in fields(payload)
        }
        return schema_class.entity_class(
            id=entity_id,
            **values,
        )
