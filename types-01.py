from typing import List, Dict, Optional, Union, Literal, TypeVar, Generic, ForwardRef
from pydantic import BaseModel, Field, validator, root_validator, conint, constr, StrictInt, StrictStr, computed_field

# 1. Basic Types
# Pydantic leverages Python's type hints to define model fields.
class User(BaseModel):
    id: int  # Integer type
    name: str  # String type
    is_active: bool  # Boolean type
    height: float  # Float type

# Example usage:
user = User(id=1, name="John Doe", is_active=True, height=1.85)

# 2. Optional Fields
# Optional fields may or may not be present. They're defined using Optional from typing.
class Profile(BaseModel):
    user_id: int
    bio: Optional[str] = None  # This field is optional and defaults to None if not provided

# Example usage:
profile1 = Profile(user_id=1, bio="Hello, world!")
profile2 = Profile(user_id=2)  # No bio provided, it will be None

# 3. Lists and Dictionaries
# You can use List and Dict from typing to define complex field types.
class Order(BaseModel):
    items: List[str]  # A list of strings
    prices: Dict[str, float]  # A dictionary with string keys and float values

# Example usage:
order = Order(
    items=["apple", "banana", "orange"],
    prices={"apple": 0.5, "banana": 0.3, "orange": 0.4}
)

# 4. Nested Models
# Models can be nested within other models.
class Address(BaseModel):
    street: str
    city: str

class AdvancedUser(BaseModel):
    name: str
    address: Address  # Using the Address model as a field type

# Example usage:
user = AdvancedUser(
    name="Jane Doe",
    address={"street": "123 Main St", "city": "Anytown"}
)

# 5. Union Types
# Union types allow a field to accept multiple types.
class Item(BaseModel):
    id: int
    value: Union[str, int, float]  # This field can be a string, integer, or float

# Example usage:
item1 = Item(id=1, value="test")
item2 = Item(id=2, value=42)
item3 = Item(id=3, value=3.14)

# 6. Literal Types
# Literal types restrict a field to a specific set of values.
class Status(BaseModel):
    status: Literal['pending', 'completed', 'failed']  # Only these three string values are allowed

# Example usage:
status1 = Status(status='pending')  # OK
# status2 = Status(status='invalid')  # This would raise a validation error

# 7. Constrained Types
# Pydantic provides constrained types to add additional validation to fields.
class ConstrainedUser(BaseModel):
    id: conint(gt=0)  # Must be an integer greater than 0
    name: constr(min_length=1, max_length=50)  # String with length between 1 and 50

# Example usage:
user = ConstrainedUser(id=1, name="John")
# user_invalid = ConstrainedUser(id=0, name="")  # This would raise a validation error

# 8. Custom Validators
# You can add custom validation logic to fields using the @validator decorator.
class ValidatedUser(BaseModel):
    name: str
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v

# Example usage:
user = ValidatedUser(name="John", password="securepass1")
# user_invalid = ValidatedUser(name="John", password="weak")  # This would raise a validation error

# 9. Field Aliases
# Field aliases allow you to use different names for fields in the JSON representation.
class AliasedUser(BaseModel):
    user_id: int = Field(..., alias='id')  # '...' means the field is required
    full_name: str = Field(..., alias='name')

# Example usage:
user = AliasedUser(id=1, name="John Doe")  # Note we use 'id' and 'name', not 'user_id' and 'full_name'

# 10. Root Validators
# Root validators allow you to validate multiple fields at once.
class Transaction(BaseModel):
    amount: float
    currency: str

    @root_validator
    def check_currency_for_amount(cls, values):
        if values.get('amount', 0) > 1000 and values.get('currency') != 'USD':
            raise ValueError('High-value transactions must be in USD')
        return values

# Example usage:
tx1 = Transaction(amount=500, currency="EUR")  # OK
tx2 = Transaction(amount=1500, currency="USD")  # OK
# tx3 = Transaction(amount=1500, currency="EUR")  # This would raise a validation error

# 11. Generic Models
# Generic models allow you to create reusable model structures.
T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    status: int

# Example usage:
class UserData(BaseModel):
    name: str
    age: int

user_response = Response[UserData](data=UserData(name="John", age=30), status=200)

# 12. Discriminated Unions
# Discriminated unions allow you to use a field to determine which model to use.
class Cat(BaseModel):
    pet_type: Literal['cat']
    meow: str

class Dog(BaseModel):
    pet_type: Literal['dog']
    bark: str

class Pet(BaseModel):
    pet: Union[Cat, Dog] = Field(..., discriminator='pet_type')

# Example usage:
cat_pet = Pet(pet={"pet_type": "cat", "meow": "Meow!"})
dog_pet = Pet(pet={"pet_type": "dog", "bark": "Woof!"})

# 13. Custom Types
# You can create custom types for reuse across your models.
EmailStr = constr(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

class EmailUser(BaseModel):
    email: EmailStr

# Example usage:
user = EmailUser(email="user@example.com")
# user_invalid = EmailUser(email="not_an_email")  # This would raise a validation error

# 14. JSON Schema Generation
# Pydantic can automatically generate JSON schemas for your models.
print(User.schema_json(indent=2))

# 15. Config and Behaviors
# You can customize model behaviors using the Config class.
class ConfiguredUser(BaseModel):
    id: int
    name: str

    class Config:
        allow_population_by_field_name = True  # Allow populating by field name and alias
        validate_assignment = True  # Validate when values are assigned, not just on model creation

# 16. Forward References
# Forward references allow you to reference a model before it's fully defined.
Node = ForwardRef('Node')

class Node(BaseModel):
    value: int
    left: Optional[Node] = None
    right: Optional[Node] = None

Node.update_forward_refs()  # This is necessary to update the forward reference

# Example usage:
root = Node(value=1, left=Node(value=2), right=Node(value=3))

# 17. Strict Types
# Strict types perform strict type checking and don't allow coercion.
class StrictUser(BaseModel):
    id: StrictInt  # Must be exactly an int, not a float or string that looks like an int
    name: StrictStr  # Must be exactly a str, not an int or float

# Example usage:
user = StrictUser(id=1, name="John")
# user_invalid = StrictUser(id="1", name="John")  # This would raise a validation error

# 18. Computed Fields
# Computed fields allow you to define fields that are calculated from other fields.
class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    def area(self) -> float:
        return self.width * self.height

# Example usage:
rect = Rectangle(width=5, height=3)
print(rect.area)  # Output: 15.0
