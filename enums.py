from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(BaseModel):
    id: int
    name: str
    status: Status

# Usage
user = User(id=1, name="John Doe", status=Status.ACTIVE)
print(user)
