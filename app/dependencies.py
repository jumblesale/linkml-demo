from uuid import uuid4

from fastapi import Depends

from app.database import entity_repository
from app.entity.id import id_generator
from app.entity.mappers import DtoDomainConverter
from app.entity.repository import EntityRepository
from app.entity.service import EntityService
from app.entity.validator import ModelValidator


def entity_service(
    repository: EntityRepository = Depends(entity_repository),
) -> EntityService:
    return EntityService(
        repository=repository,
        converter=DtoDomainConverter(),
        id_generator=id_generator,
        validator=ModelValidator(),
    )
