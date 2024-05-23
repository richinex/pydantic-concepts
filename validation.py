from pydantic import BaseModel, ValidationError, conint

class User(BaseModel):
    id: conint(gt=0)
    name: str
    age: conint(ge=18)

# Usage
try:
    user = User(id=1, name="John Doe", age=17)
except ValidationError as e:
    print(e)
