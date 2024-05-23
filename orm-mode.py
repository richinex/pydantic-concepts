from pydantic import BaseModel

class UserORM:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Usage
user_orm = UserORM(id=1, name="John Doe")
user = User.from_orm(user_orm)
print(user)
