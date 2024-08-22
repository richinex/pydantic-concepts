# serialization

import json
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime, date
from enum import Enum
from uuid import UUID
import yaml  # You might need to install pyyaml: pip install pyyaml

# Let's start with some basic models

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class User(BaseModel):
    id: UUID
    username: str
    email: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None
    address: Address

    # Custom serialization method
    def json(self, **kwargs):
        # Convert to dict, then to JSON string
        return json.dumps(self.dict(), default=str, **kwargs)

    # Custom deserialization method
    @classmethod
    def parse_raw(cls, raw_data):
        # Parse JSON string to dict, then create User instance
        data = json.loads(raw_data)
        return cls(**data)

# Now, let's create a more complex model that includes nested structures and custom serialization logic

class Tag(BaseModel):
    id: int
    name: str

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class Product(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    category: Category
    tags: List[Tag]
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_available: bool = True

    class Config:
        # This allows the model to use alias names for fields
        allow_population_by_field_name = True

        # Custom JSON encoders for specific types
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }

    # Custom validator for price
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return round(v, 2)  # Round to 2 decimal places

    # Root validator to ensure updated_at is after created_at
    @root_validator
    def check_timestamps(cls, values):
        created_at, updated_at = values.get('created_at'), values.get('updated_at')
        if updated_at and created_at and updated_at < created_at:
            raise ValueError('updated_at must be after created_at')
        return values

# Now, let's demonstrate various serialization and deserialization scenarios

def serialize_deserialize_examples():
    # Create a sample user
    user = User(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        username="johndoe",
        email="john@example.com",
        role=UserRole.USER,
        created_at=datetime.now(),
        address=Address(
            street="123 Main St",
            city="Anytown",
            country="USA",
            postal_code="12345"
        )
    )

    print("1. Basic JSON serialization:")
    user_json = user.json(indent=2)
    print(user_json)

    print("\n2. Deserialization from JSON:")
    deserialized_user = User.parse_raw(user_json)
    print(f"Deserialized user: {deserialized_user}")

    print("\n3. Dict serialization:")
    user_dict = user.dict()
    print(json.dumps(user_dict, default=str, indent=2))

    print("\n4. Serialization with include/exclude:")
    print(user.json(include={'username', 'email'}, indent=2))
    print(user.json(exclude={'id', 'created_at'}, indent=2))

    # Create a sample product
    product = Product(
        id=UUID('87654321-8765-4321-8765-432187654321'),
        name="Awesome Product",
        description="This is an awesome product",
        price=99.99,
        category=Category(id=1, name="Electronics"),
        tags=[Tag(id=1, name="tech"), Tag(id=2, name="gadget")],
        created_at=datetime.now()
    )

    print("\n5. Product serialization with custom JSON encoders:")
    product_json = product.json(indent=2)
    print(product_json)

    print("\n6. Deserialization with custom parsing:")
    deserialized_product = Product.parse_raw(product_json)
    print(f"Deserialized product: {deserialized_product}")

    print("\n7. YAML serialization:")
    product_dict = product.dict()
    yaml_string = yaml.dump(product_dict, default_flow_style=False)
    print(yaml_string)

    print("\n8. Deserialization from YAML:")
    yaml_dict = yaml.safe_load(yaml_string)
    deserialized_product_from_yaml = Product(**yaml_dict)
    print(f"Deserialized product from YAML: {deserialized_product_from_yaml}")

    print("\n9. Partial update using dict:")
    update_data = {'price': 89.99, 'is_available': False}
    updated_product = product.copy(update=update_data)
    print(f"Updated product: {updated_product}")

    print("\n10. Serialization to CSV-friendly format:")
    def flatten_product(product: Product) -> Dict:
        flat = product.dict()
        flat['category_id'] = flat['category']['id']
        flat['category_name'] = flat['category']['name']
        flat['tags'] = ','.join(tag['name'] for tag in flat['tags'])
        del flat['category']
        return flat

    flattened = flatten_product(product)
    print(json.dumps(flattened, default=str, indent=2))

if __name__ == "__main__":
    serialize_deserialize_examples()
    
    
This example covers various aspects of serialization, marshalling, and unmarshalling using Pydantic. Here's a breakdown of what's demonstrated:

Basic JSON serialization: Shows how to convert a Pydantic model to a JSON string.
Deserialization from JSON: Demonstrates how to parse a JSON string back into a Pydantic model.
Dict serialization: Converts a Pydantic model to a Python dictionary.
Selective serialization: Shows how to include or exclude specific fields during serialization.
Custom JSON encoders: Demonstrates how to handle custom types (like datetime and UUID) during JSON serialization.
Custom deserialization: Shows how to parse a JSON string with custom types back into a Pydantic model.
YAML serialization: Converts a Pydantic model to a YAML string.
Deserialization from YAML: Demonstrates how to parse a YAML string back into a Pydantic model.
Partial updates: Shows how to update a model partially using a dictionary.
CSV-friendly serialization: Demonstrates how to flatten a nested structure for CSV export.

This example also includes:

Custom validation logic using @validator and @root_validator decorators.
Use of Enum for predefined choices (UserRole).
Nested models (Address within User, Category and Tags within Product).
Optional fields with default values.
Custom configuration options in the Config class.

These examples cover a wide range of serialization and deserialization scenarios you might encounter when working with Pydantic models. They demonstrate how Pydantic makes it easy to convert between different data formats while maintaining data integrity and type safety.
