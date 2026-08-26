from uuid import uuid4

from fastapi import Depends

from app.database import get_repository
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository
from app.entity.service import EntityService
from app.entity.validator import ModelValidator


def get_service(
    repository: EntityRepository = Depends(get_repository),
) -> EntityService:
    return EntityService(
        repository=repository,
        converter=DtoDomainConverter(),
        id_generator=lambda: str(uuid4()),
        validator=ModelValidator(),
    )
