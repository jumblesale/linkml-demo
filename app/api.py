from http import HTTPStatus
from collections.abc import Callable
from urllib.parse import quote

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from bookstore.generated.schema import SchemaClassAddressable
from app.entity.service import EntityService
from app.entity.exceptions import (
    EntityNotFound,
    RelatedEntityNotFound,
    UniqueConstraintViolation,
)


class ConflictResponse(BaseModel):
    field: str

def _schema_classes() -> list[type[SchemaClassAddressable]]:
    return sorted([
        schema_class
        for schema_class in SchemaClassAddressable.__subclasses__()
    ], key=lambda schema_class: schema_class.__name__)

class Api:
    def __init__(
        self,
        app: FastAPI,
        service_dependency: Callable[..., EntityService],
    ):
        self.app = app
        self.service_dependency = service_dependency
        self.app.add_exception_handler(
            UniqueConstraintViolation,
            self.unique_constraint_handler,
        )
        self.app.add_exception_handler(
            RelatedEntityNotFound,
            self.related_entity_not_found_handler,
        )
        self.app.add_exception_handler(
            EntityNotFound,
            self.entity_not_found_handler,
        )
        self.register_handlers()

    @staticmethod
    async def unique_constraint_handler(
        _: Request,
        exception: Exception,
    ) -> JSONResponse:
        assert isinstance(exception, UniqueConstraintViolation)
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={"field": exception.field},
        )

    @staticmethod
    async def related_entity_not_found_handler(
        _: Request,
        exception: Exception,
    ) -> JSONResponse:
        assert isinstance(exception, RelatedEntityNotFound)
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={
                "relationship": exception.relationship,
                "id": exception.entity_id,
            },
        )

    @staticmethod
    async def entity_not_found_handler(
        _: Request,
        exception: Exception,
    ) -> JSONResponse:
        assert isinstance(exception, EntityNotFound)
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": str(exception)},
        )


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

    def delete_handler(
        self,
        schema_class: type[SchemaClassAddressable],
    ):
        def _delete_handler(
            entity_id: str,
            service: EntityService = Depends(self.service_dependency),
        ):
            service.delete(
                schema_class=schema_class,
                entity_id=entity_id,
            )
            return Response(status_code=HTTPStatus.NO_CONTENT)

        _delete_handler.__name__ = f"delete_{schema_class.api_resource_name}"
        return _delete_handler

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
                responses={
                    HTTPStatus.CONFLICT: {
                        "model": ConflictResponse,
                        "description": "A unique field value already exists.",
                    },
                },
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

            self.app.delete(
                f"/{schema_class.api_resource_name}/{{entity_id}}",
                name=f"delete_{schema_class.api_resource_name}",
                summary=f"Delete a {schema_class.entity_name()} by id",
                tags=[schema_class.__name__],
                status_code=HTTPStatus.NO_CONTENT,
            )(self.delete_handler(schema_class))
