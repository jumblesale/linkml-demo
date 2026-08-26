from uuid import uuid4

from fastapi import FastAPI

from app.api import Api
from app.entity.converter import EntityConverter
from app.entity.repository import EntityRepository
from app.entity.service import EntityService


fast_api =  FastAPI(title="Bookstore API")
api = Api(
    app=fast_api,
    entity_service=EntityService(
        repository=EntityRepository(),
        converter=EntityConverter(),
        id_generator=lambda: str(uuid4()),
    ),
)
