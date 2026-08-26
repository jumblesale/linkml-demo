from typing import TypeVar

from bookstore.generated.entity import Base


Entity = TypeVar("Entity", bound=Base)


class EntityRepository:
    def __init__(self):
        self.entities: list[Base] = []

    def save(self, entity: Entity) -> Entity:
        self.entities.append(entity)
        return entity
