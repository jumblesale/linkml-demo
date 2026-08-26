from contextlib import asynccontextmanager
from fastapi import FastAPI

from bookstore.generated.constraints import apply_constraints
from app.api import Api
from app.database import engine
from app.dependencies import get_service
from bookstore.generated.entity import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


fast_api = FastAPI(title="Bookstore API", lifespan=lifespan)
apply_constraints()
api = Api(
    app=fast_api,
    service_dependency=get_service,
)
