from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool

# Usage
user = User(id=1, name="John Doe", is_active=True)
print(user)
print(user.dict())
