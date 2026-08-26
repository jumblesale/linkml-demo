from bookstore.generated.entity import Base, Model


class EntityRepository:
    def __init__(self):
        self.entities: list[Model] = []

    def save(self, entity: Model) -> None:
        self.entities.append(entity)

    def find_all(self) -> list[Model]:
        return self.entities

    def find_by_id(self, entity_id: str) -> Model | None:
        entity = next(
            (
                entity
                for entity in self.entities
                if entity.id == entity_id
            ),
            None,
        )
        return entity
