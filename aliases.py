from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    full_name: str = Field(..., alias="name")

# Usage
data = {"id": 1, "name": "John Doe"}
user = User(**data)
print(user)
