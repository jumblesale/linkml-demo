from http import HTTPStatus
from collections.abc import Callable
from urllib.parse import quote

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

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
        service_dependency: Callable[..., EntityService],
    ):
        self.app = app
        self.service_dependency = service_dependency
        self.register_handlers()


    def post_handler(
        self,
        schema_class: type[SchemaClassAddressable],
    ):
        def _post_handler(
            payload,
            service: EntityService = Depends(self.service_dependency),
        ) -> Response:
            entity_id = service.create(
                schema_class=schema_class,
                payload=payload,
            )
            location = f"/{schema_class.api_resource_name}/{quote(entity_id, safe='')}"
            return Response(
                status_code=HTTPStatus.CREATED,
                headers={"Location": location},
            )

        _post_handler.__annotations__["payload"] = schema_class.write_model
        _post_handler.__name__ = f"create_{schema_class.api_resource_name}"
        return _post_handler

    def get_handler(
        self,
        schema_class: type[SchemaClassAddressable],
    ):
        def _get_handler(
            entity_id: str,
            service: EntityService = Depends(self.service_dependency),
        ):
            read_model = service.get(
                schema_class=schema_class,
                entity_id=entity_id,
            )
            if read_model is None:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
            return read_model

        _get_handler.__name__ = f"get_{schema_class.api_resource_name}"
        return _get_handler

    def get_all_handler(
        self,
        schema_class: type[SchemaClassAddressable],
    ):
        def _get_all_handler(
            service: EntityService = Depends(self.service_dependency),
        ):
            return service.get_all(
                schema_class=schema_class,
            )

        _get_all_handler.__name__ = f"get_all_{schema_class.api_resource_name}"
        return _get_all_handler

    def register_handlers(
        self,
    ):
        for schema_class in _schema_classes():
            self.app.post(
                f"/{schema_class.api_resource_name}",
                name=f"create_{schema_class.api_resource_name}",
                summary=f"Create a new {schema_class.entity_name()}",
                tags=[schema_class.__name__],
                status_code=HTTPStatus.CREATED,
            )(self.post_handler(schema_class))
            
            self.app.get(
                f"/{schema_class.api_resource_name}",
                name=f"get_all_{schema_class.api_resource_name}",
                summary=f"Get all {schema_class.entity_name()}s",
                tags=[schema_class.__name__],
                response_model=list[schema_class.read_model],
            )(self.get_all_handler(schema_class))

            self.app.get(
                f"/{schema_class.api_resource_name}/{{entity_id}}",
                name=f"get_{schema_class.api_resource_name}",
                summary=f"Get a {schema_class.entity_name()} by id",
                tags=[schema_class.__name__],
                response_model=schema_class.read_model,
            )(self.get_handler(schema_class))
