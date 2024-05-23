from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

    class Config:
        allow_mutation = False

# Usage
user = User(id=1, name="John Doe")
try:
    user.id = 2
except TypeError as e:
    print(e)
