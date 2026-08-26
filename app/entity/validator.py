from dataclasses import Field, asdict, fields
from re import Pattern
from typing import Any

from fastapi.exceptions import RequestValidationError

from bookstore.generated.domain import Model, slots
from bookstore.generated.schema import SchemaClassAddressable


class ModelValidator:
    def validate(
        self,
        schema_class: type[SchemaClassAddressable],
        model: Model,
    ) -> None:
        instance = asdict(model)
        errors = [
            error
            for field in fields(model)
            for error in self._validate_field(model, field)
        ]
        errors.extend(self._validate_relationships(schema_class, model))

        if errors:
            raise RequestValidationError(
                errors,
                body=instance,
            )

    @staticmethod
    def _validate_relationships(
        schema_class: type[SchemaClassAddressable],
        model: Model,
    ) -> list[dict[str, Any]]:
        return [
            ModelValidator._cardinality_error(
                field_name=name,
                value=value,
                minimum=minimum,
            )
            for name, relationship in schema_class.relationships.items()
            if (minimum := relationship.minimum_cardinality) is not None
            for value in (getattr(model, name, None),)
            if ModelValidator._value_count(value) < minimum
        ]

    @staticmethod
    def _value_count(value: Any) -> int:
        return len(value) if isinstance(value, list) else int(value is not None)

    @staticmethod
    def _cardinality_error(
        field_name: str,
        value: Any,
        minimum: int,
    ) -> dict[str, Any]:
        return ModelValidator._validation_error(
            error_type="too_short",
            location=("body", field_name),
            message=f"List should have at least {minimum} item(s)",
            value=value,
            context={"min_length": minimum},
        )

    def _validate_field(
        self,
        model: Model,
        field: Field[Any],
    ) -> list[dict[str, Any]]:
        value = getattr(model, field.name)
        pattern = self._pattern_for(field.name)
        if value is None or pattern is None:
            return []

        return self._pattern_errors(pattern, field.name, value)

    @staticmethod
    def _pattern_for(field_name: str) -> Pattern[str] | None:
        slot = getattr(slots, field_name, None)
        pattern = getattr(slot, "pattern", None)
        return pattern if isinstance(pattern, Pattern) else None

    def _pattern_errors(
        self,
        pattern: Pattern[str],
        field_name: str,
        value: Any,
    ) -> list[dict[str, Any]]:
        values = value if isinstance(value, list) else [value]
        return [
            self._pattern_error(
                pattern,
                item,
                self._location(field_name, value, index),
            )
            for index, item in enumerate(values)
            if pattern.fullmatch(str(item)) is None
        ]

    @staticmethod
    def _location(
        field_name: str,
        value: Any,
        index: int,
    ) -> tuple[Any, ...]:
        location = ("body", field_name)
        return location + (index,) if isinstance(value, list) else location

    @staticmethod
    def _pattern_error(
        pattern: Pattern[str],
        value: Any,
        location: tuple[Any, ...],
    ) -> dict[str, Any]:
        return ModelValidator._validation_error(
            error_type="string_pattern_mismatch",
            location=location,
            message=f"String should match pattern '{pattern.pattern}'",
            value=value,
            context={"pattern": pattern.pattern},
        )

    @staticmethod
    def _validation_error(
        error_type: str,
        location: tuple[Any, ...],
        message: str,
        value: Any,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "type": error_type,
            "loc": location,
            "msg": message,
            "input": value,
            "ctx": context,
        }