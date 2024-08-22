from typing import List, Dict, Optional, Union, Literal, TypeVar, Generic, Tuple, Set, Callable, Any, Type
from pydantic import BaseModel, Field, validator, root_validator, conint, constr, StrictInt, StrictStr, computed_field, PrivateAttr
from pydantic.generics import GenericModel
from datetime import datetime, date
from uuid import UUID
from enum import Enum
import re

# 1. Complex Nested Structures
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class ContactInfo(BaseModel):
    email: str
    phone: Optional[str] = None

class User(BaseModel):
    id: UUID
    name: str
    address: Address
    contact: ContactInfo
    created_at: datetime

# Example usage:
user = User(
    id="123e4567-e89b-12d3-a456-426614174000",
    name="John Doe",
    address={
        "street": "123 Main St",
        "city": "Anytown",
        "country": "USA",
        "postal_code": "12345"
    },
    contact={
        "email": "john@example.com",
        "phone": "+1234567890"
    },
    created_at="2023-06-01T12:00:00"
)

# 2. Enums and Literal Types
class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class UserStatus(BaseModel):
    role: UserRole
    is_active: bool
    account_type: Literal["free", "premium", "enterprise"]

# Example usage:
status = UserStatus(role=UserRole.ADMIN, is_active=True, account_type="premium")

# 3. Complex Validations
class Product(BaseModel):
    name: str
    price: float
    stock: int
    tags: Set[str]

    @validator('name')
    def name_must_be_capitalized(cls, v):
        return v.capitalize()

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    @root_validator
    def check_stock_and_tags(cls, values):
        if values.get('stock', 0) > 0 and 'in_stock' not in values.get('tags', []):
            values['tags'].add('in_stock')
        return values

# Example usage:
product = Product(name="laptop", price=999.99, stock=10, tags={"electronics", "computers"})
print(product.name)  # Output: Laptop
print(product.tags)  # Output: {'electronics', 'computers', 'in_stock'}

# 4. Generic Models with Constraints
T = TypeVar('T')

class Paginated(GenericModel, Generic[T]):
    items: List[T]
    page: conint(gt=0)
    total_pages: conint(gt=0)

class UserSummary(BaseModel):
    id: int
    name: str

# Example usage:
paginated_users = Paginated[UserSummary](
    items=[
        UserSummary(id=1, name="Alice"),
        UserSummary(id=2, name="Bob")
    ],
    page=1,
    total_pages=5
)

# 5. Custom Types and Validators
class HexColor(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = re.match(r'^#[0-9A-Fa-f]{6}$', v)
        if not m:
            raise ValueError('invalid hex color format')
        return cls(v)

class Theme(BaseModel):
    primary_color: HexColor
    secondary_color: HexColor

# Example usage:
theme = Theme(primary_color="#FF0000", secondary_color="#00FF00")

# 6. Unions with Different Types
class Notification(BaseModel):
    id: int
    content: Union[str, Dict[str, Any]]
    created_at: datetime

# Example usage:
text_notification = Notification(id=1, content="Hello, world!", created_at="2023-06-01T12:00:00")
json_notification = Notification(id=2, content={"title": "New message", "body": "You have a new message"}, created_at="2023-06-01T12:00:00")

# 7. Recursive Models
class Comment(BaseModel):
    id: int
    content: str
    replies: List['Comment'] = []

Comment.update_forward_refs()

# Example usage:
comment = Comment(
    id=1,
    content="Great post!",
    replies=[
        Comment(id=2, content="Thanks!", replies=[
            Comment(id=3, content="You're welcome!")
        ])
    ]
)

# 8. Models with Callable Fields
class Task(BaseModel):
    name: str
    execute: Callable[[], None]

def say_hello():
    print("Hello, world!")

# Example usage:
task = Task(name="Greeting", execute=say_hello)
task.execute()  # Output: Hello, world!

# 9. Advanced Config Options
class AdvancedUser(BaseModel):
    id: int
    name: str
    _secret: str = PrivateAttr()

    class Config:
        allow_mutation = False
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __init__(self, **data):
        super().__init__(**data)
        self._secret = "some_secret_value"

# Example usage:
user = AdvancedUser(id=1, name="Alice")
# user.name = "Bob"  # This would raise an error due to allow_mutation = False

# 10. Complex Inheritance
class BaseEvent(BaseModel):
    id: UUID
    timestamp: datetime

class UserEvent(BaseEvent):
    user_id: int

class LoginEvent(UserEvent):
    ip_address: str

class PurchaseEvent(UserEvent):
    product_id: int
    amount: float

# Example usage:
login_event = LoginEvent(
    id="123e4567-e89b-12d3-a456-426614174000",
    timestamp="2023-06-01T12:00:00",
    user_id=1,
    ip_address="192.168.1.1"
)

# 11. Dynamic Model Creation
def create_model_class(name: str, **field_definitions):
    return type(name, (BaseModel,), field_definitions)

# Example usage:
DynamicUser = create_model_class("DynamicUser", name=(str, ...), age=(int, ...))
dynamic_user = DynamicUser(name="Alice", age=30)

# 12. Complex Computed Fields
class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

    @computed_field
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Example usage:
rect = Rectangle(width=5, height=3)
print(f"Area: {rect.area}, Perimeter: {rect.perimeter}")

# 13. Type Coercion and Strict Types
class MixedTypes(BaseModel):
    flexible_int: int  # Will attempt to coerce strings to int
    strict_int: StrictInt  # Will only accept actual integers
    flexible_bool: bool  # Will coerce various values to bool
    strict_bool: StrictStr  # Will only accept actual booleans

# Example usage:
mixed = MixedTypes(
    flexible_int="123",
    strict_int=456,
    flexible_bool="true",
    strict_bool=True
)

# 14. Complex Date and Time Handling
class DateTimeModel(BaseModel):
    start_date: date
    end_date: date
    duration: Tuple[int, int, int]  # (hours, minutes, seconds)

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

    @computed_field
    @property
    def duration_seconds(self) -> int:
        hours, minutes, seconds = self.duration
        return hours * 3600 + minutes * 60 + seconds

# Example usage:
dt_model = DateTimeModel(
    start_date="2023-06-01",
    end_date="2023-06-05",
    duration=(48, 30, 15)
)
print(f"Duration in seconds: {dt_model.duration_seconds}")

# 15. Complex Discriminated Unions
class Shape(BaseModel):
    type: str

class Circle(Shape):
    type: Literal['circle']
    radius: float

class Rectangle(Shape):
    type: Literal['rectangle']
    width: float
    height: float

class ComplexShape(BaseModel):
    shape: Union[Circle, Rectangle] = Field(..., discriminator='type')

# Example usage:
circle_shape = ComplexShape(shape={"type": "circle", "radius": 5.0})
rectangle_shape = ComplexShape(shape={"type": "rectangle", "width": 10.0, "height": 5.0})


This extended guide covers a wide range of Pydantic use cases and advanced typing combinations. It demonstrates how to:

Create complex nested structures
Use enums and literal types
Implement complex validations
Create generic models with constraints
Define and use custom types with validators
Work with unions of different types
Create recursive models
Use callable fields in models
Utilize advanced configuration options
Implement complex inheritance structures
Create models dynamically
Use complex computed fields
Handle type coercion and strict types
Work with complex date and time scenarios
Implement complex discriminated unions

These examples showcase the flexibility and power of Pydantic in handling a wide variety of data modeling and validation scenarios. By mastering these concepts, you'll be well-equipped to handle even the most complex data structures and validation requirements in your Python projects.
