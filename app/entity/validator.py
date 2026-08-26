from dataclasses import Field, asdict, fields
from re import Pattern
from typing import Any

from fastapi.exceptions import RequestValidationError

from bookstore.generated.domain import Model, slots


class ModelValidator:
    def validate(self, model: Model) -> None:
        instance = asdict(model)
        errors = [
            error
            for field in fields(model)
            for error in self._validate_field(model, field)
        ]

        if errors:
            raise RequestValidationError(
                errors,
                body=instance,
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
            self._error(pattern, item, self._location(field_name, value, index))
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
    def _error(
        pattern: Pattern[str],
        value: Any,
        location: tuple[Any, ...],
    ) -> dict[str, Any]:
        return {
            "type": "string_pattern_mismatch",
            "loc": location,
            "msg": f"String should match pattern '{pattern.pattern}'",
            "input": value,
            "ctx": {"pattern": pattern.pattern},
        }