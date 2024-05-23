from pydantic import BaseModel, validator

class User(BaseModel):
    id: int
    name: str
    email: str

    @validator('email')
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError('Invalid email')
        return v

# Usage
try:
    user = User(id=1, name="John Doe", email="johndoe.com")
except ValidationError as e:
    print(e)
