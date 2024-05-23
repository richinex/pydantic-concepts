from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

# Usage
user = User(id=1, name="John Doe")
print(user.json())
