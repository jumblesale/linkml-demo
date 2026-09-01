from datetime import UTC, datetime

from app.entity.id import Identifier, IdGenerator
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository
from app.entity.validator import ModelValidator
from bookstore.generated.dto import DTOCreate, DTORead
from bookstore.generated.schema import SchemaClassAddressable


class EntityService:
    def __init__(
        self,
        repository: EntityRepository,
        converter: DtoDomainConverter,
        id_generator: IdGenerator,
        validator: ModelValidator,
    ):
        self.repository = repository
        self.converter = converter
        self.id_generator = id_generator
        self.validator = validator

    def _relationship_overrides(
        self,
        schema_class: type[SchemaClassAddressable],
        payload: DTOCreate,
    ) -> dict[str, object]:
        overrides: dict[str, object] = {}
        for name, relationship in schema_class.relationships.items():
            if not hasattr(payload, name):
                continue
            relationship_value = getattr(payload, name)
            if relationship_value is None:
                continue
            target_schema_class = self.repository._target_schema_class(
                relationship.target_class_name,
            )
            values = relationship_value if relationship.multivalued else [relationship_value]
            related_models = [
                self.repository.find_by_id(target_schema_class, str(value))
                for value in values
            ]
            if any(model is None for model in related_models):
                missing = next(
                    str(value)
                    for value, model in zip(values, related_models, strict=True)
                    if model is None
                )
                raise self.repository._find_related_entity(
                    name,
                    target_schema_class,
                    missing,
                )
            overrides[name] = (
                related_models if relationship.multivalued else related_models[0]
            )
        return overrides

    def create(
        self,
        schema_class: type[SchemaClassAddressable],
        payload: DTOCreate,
    ) -> Identifier:
        self.validator.validate(schema_class, payload)
        model = self.converter.to_domain(
            schema_class=schema_class,
            payload=payload,
            entity_id=(id := self.id_generator()),
            created_at=datetime.now(UTC),
            **self._relationship_overrides(schema_class, payload),
        )
        self.validator.validate(schema_class, model)
        self.repository.save(schema_class, model)
        return id

    def get(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> DTORead | None:
        if (model := self.repository.find_by_id(schema_class, entity_id)) is None:
            return None
        return self.converter.to_dto(schema_class, model)

    def get_all(
        self,
        schema_class: type[SchemaClassAddressable],
    ) -> list[DTORead]:
        return [
            self.converter.to_dto(schema_class, model)
            for model in self.repository.find_all(schema_class)
        ]

    def delete(
        self,
        schema_class: type[SchemaClassAddressable],
        entity_id: Identifier,
    ) -> None:
        self.repository.delete(
            schema_class=schema_class,
            entity_id=entity_id,
        )
