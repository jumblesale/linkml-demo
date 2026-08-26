from typing import Callable, TypeAlias
from uuid import uuid4

Identifier: TypeAlias = str
IdGenerator = Callable[[], Identifier]

def id() -> Identifier:
    return str(uuid4())
