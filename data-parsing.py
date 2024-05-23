from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool

# Usage
data = {"id": "1", "name": "John Doe", "is_active": "true"}
user = User.parse_obj(data)
print(user)
