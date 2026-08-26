from uuid import uuid4

from fastapi import FastAPI

from bookstore.generated.constraints import apply_constraints
from app.api import Api
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository
from app.entity.service import EntityService
from app.entity.validator import ModelValidator


fast_api =  FastAPI(title="Bookstore API")
apply_constraints()
api = Api(
    app=fast_api,
    entity_service=EntityService(
        repository=EntityRepository(),
        converter=DtoDomainConverter(),
        id_generator=lambda: str(uuid4()),
        validator=ModelValidator(),
    ),
)
