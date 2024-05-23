from pydantic import BaseModel
from typing import List, Dict

class User(BaseModel):
    id: int
    name: str
    tags: List[str]
    profile: Dict[str, str]

# Usage
user = User(id=1, name="John Doe", tags=["python", "developer"], profile={"twitter": "@johndoe"})
print(user)
