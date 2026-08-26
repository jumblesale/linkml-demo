from bookstore.generated.entity import Base


class EntityRepository:
    def __init__(self):
        self.entities: list[Base] = []

    def save(self, entity: Base) -> None:
        self.entities.append(entity)

    def find_by_id(self, entity_id: str) -> Base | None:
        return next(
            (
                entity
                for entity in self.entities
                if getattr(entity, "id", None) == entity_id
            ),
            None,
        )
