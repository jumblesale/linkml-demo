class UniqueConstraintViolation(Exception):
    def __init__(self, field: str):
        super().__init__(f"A value for '{field}' already exists")
        self.field = field
