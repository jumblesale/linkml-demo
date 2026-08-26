from dataclasses import fields

from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.entity import Base
from bookstore.generated.schema import SchemaClassAddressable


class EntityConverter:
    def to_entity(
        self,
        schema_class: type[SchemaClassAddressable],
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

    def to_read_model(
        self,
        schema_class: type[SchemaClassAddressable],
        entity: Base,
    ) -> DTORead:
        values = {
            field.name: getattr(entity, field.name)
            for field in fields(schema_class.read_model)
        }
        return schema_class.read_model(**values)
