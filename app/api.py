from http import HTTPStatus
from urllib.parse import quote

from fastapi import FastAPI, Response

from bookstore.generated.schema import SchemaClass
from app.entity.service import EntityService

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
        def _post_handler(payload) -> Response:
            entity = self.entity_service.create(
                schema_class=schema_class,
                payload=payload,
            )
            location = (
                f"/{schema_class.api_resource_name}/{quote(str(entity.id), safe='')}"
            )
            return Response(
                status_code=HTTPStatus.CREATED,
                headers={"Location": location},
            )

        _post_handler.__annotations__["payload"] = schema_class.write_model
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
