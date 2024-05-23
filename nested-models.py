from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str

class User(BaseModel):
    id: int
    name: str
    address: Address

# Usage
address = Address(city="New York", state="NY")
user = User(id=1, name="John Doe", address=address)
print(user)
print(user.address.city)
