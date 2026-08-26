from typing import Type, TypeVar

from bookstore.generated.model import Model

T = TypeVar("T", bound=Model)

def to_model(
    model_class: Type[T],
    payload: dict,
) -> T:
    ...

def to_json(
    model: Model
) -> dict:
    ...
