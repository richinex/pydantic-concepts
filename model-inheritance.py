from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    is_active: bool

# Usage
user_create = UserCreate(id=1, name="John Doe", password="secret")
user = User(id=1, name="John Doe", is_active=True)
print(user_create)
print(user)
