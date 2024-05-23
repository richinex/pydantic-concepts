from pydantic import BaseModel
import json

class User(BaseModel):
    id: int
    name: str

# Usage
json_data = '{"id": 1, "name": "John Doe"}'
user = User.parse_raw(json_data)
print(user)
