from contextlib import asynccontextmanager
from fastapi import FastAPI

from bookstore.generated.constraints import apply_constraints
from app.api import Api
from app.database import engine
from app.dependencies import entity_service
from bookstore.generated.entity import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    apply_constraints()
    Base.metadata.create_all(bind=engine)
    yield


fast_api = FastAPI(title="Bookstore API", lifespan=lifespan)
api = Api(
    app=fast_api,
    service_dependency=entity_service,
)
