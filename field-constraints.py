from pydantic import BaseModel, conint, constr

class User(BaseModel):
    id: conint(gt=0)
    name: constr(min_length=3, max_length=50)

# Usage
try:
    user = User(id=1, name="Jo")
except ValidationError as e:
    print(e)
