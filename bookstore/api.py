from http import HTTPStatus
from typing import Any

from fastapi import FastAPI

from bookstore.generated.schema import SchemaClass
from bookstore.json import to_model
from bookstore.service import EntityService

app = FastAPI(title="Bookstore API")

def _schema_classes() -> list[type[SchemaClass]]:
    return [
        schema_class for schema_class in SchemaClass.__subclasses__()
        if schema_class.api_resource_name
    ]

class Api:
    def __init__(
        self,
        app: FastAPI,
        entity_service: EntityService,
    ):
        self.app = app
        self.entity_service = entity_service
        self.register_handlers()


    def post_handler(
        self,
        schema_class: type[SchemaClass],
    ):
        def _post_handler(payload: dict[str, Any]):
            model = to_model(
                model_class=schema_class.model_class,
                payload=payload,
            )
            self.entity_service.create(
                schema_class=schema_class,
                model=model,
            )
        
        _post_handler.__name__ = f"create_{schema_class.api_resource_name}"
        return _post_handler

    def register_handlers(
        self,
    ):
        for schema_class in _schema_classes():
            self.app.post(
                f"/{schema_class.api_resource_name}",
                name=f"create_{schema_class.api_resource_name}",
                status_code=HTTPStatus.CREATED,
            )(self.post_handler(schema_class))
