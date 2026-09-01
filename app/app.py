import json
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from bookstore.generated.constraints import apply_constraints
from app.api import Api
from app.database import engine
from app.dependencies import entity_service
from bookstore.generated.entity import Base


class SortedJSONResponse(JSONResponse):
    """JSON response that sorts keys alphabetically."""
    def render(self, content: Any) -> bytes:
        # Convert Pydantic models and other types to JSON-serializable dicts
        content = jsonable_encoder(content)
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


@asynccontextmanager
async def lifespan(_: FastAPI):
    apply_constraints()
    Base.metadata.create_all(bind=engine)
    yield


fast_api = FastAPI(
    title="Bookstore API",
    lifespan=lifespan,
    default_response_class=SortedJSONResponse,
)
api = Api(
    app=fast_api,
    service_dependency=entity_service,
)
