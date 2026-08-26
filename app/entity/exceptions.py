class UniqueConstraintViolation(Exception):
    def __init__(self, field: str):
        super().__init__(f"A value for '{field}' already exists")
        self.field = field


class RelatedEntityNotFound(Exception):
    def __init__(self, relationship: str, entity_id: str):
        super().__init__(
            f"No entity with id '{entity_id}' was found for '{relationship}'"
        )
        self.relationship = relationship
        self.entity_id = entity_id
