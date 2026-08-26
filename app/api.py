from http import HTTPStatus
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, Response

from bookstore.generated.schema import SchemaClassAddressable
from app.entity.service import EntityService

def _schema_classes() -> list[type[SchemaClassAddressable]]:
    return [
        schema_class
        for schema_class in SchemaClassAddressable.__subclasses__()
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
        schema_class: type[SchemaClassAddressable],
    ):
        def _post_handler(payload) -> Response:
            entity_id = self.entity_service.create(
                schema_class=schema_class,
                payload=payload,
            )
            location = f"/{schema_class.api_resource_name}/{quote(entity_id, safe='')}"
            return Response(
                headers={"Location": location},
            )

        _post_handler.__annotations__["payload"] = schema_class.write_model
        _post_handler.__name__ = f"create_{schema_class.api_resource_name}"
        return _post_handler

    def get_handler(
        self,
        schema_class: type[SchemaClassAddressable],
    ):
        def _get_handler(entity_id: str):
            read_model = self.entity_service.get(
                schema_class=schema_class,
                entity_id=entity_id,
            )
            if read_model is None:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
            return read_model

        _get_handler.__name__ = f"get_{schema_class.api_resource_name}"
        return _get_handler

    def register_handlers(
        self,
    ):
        for schema_class in _schema_classes():
            self.app.post(
                f"/{schema_class.api_resource_name}",
                name=f"create_{schema_class.api_resource_name}",
                status_code=HTTPStatus.CREATED,
            )(self.post_handler(schema_class))
            self.app.get(
                f"/{schema_class.api_resource_name}/{{entity_id}}",
                name=f"get_{schema_class.api_resource_name}",
                response_model=schema_class.read_model,
            )(self.get_handler(schema_class))
