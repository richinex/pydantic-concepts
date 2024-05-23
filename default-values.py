from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool = True

# Usage
user = User(id=1, name="John Doe")
print(user.is_active)  # Output: True
