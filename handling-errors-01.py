# Error handling 01
from pydantic import BaseModel, ValidationError, validator, root_validator, constr, conint, EmailStr, Field
from typing import List, Optional, Dict
from datetime import date, datetime
import json

# Custom exception for business logic errors
class BusinessLogicError(Exception):
    pass

# 1. Basic Model with Validators
class User(BaseModel):
    id: int
    username: constr(min_length=3, max_length=50)  # Constrained string
    email: EmailStr
    age: conint(ge=18, le=120)  # Constrained integer (greater than or equal to 18, less than or equal to 120)
    
    # Field-level validator
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    # Model-level validator
    @root_validator
    def check_email_domain(cls, values):
        email = values.get('email')
        if email and not email.endswith('@company.com'):
            raise ValueError('Email must be a company email')
        return values

# 2. Nested Model with Error Propagation
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Employee(BaseModel):
    user: User
    department: str
    address: Address
    hire_date: date

# 3. Model with Custom Error Handling
class Project(BaseModel):
    name: str
    start_date: date
    end_date: date
    budget: float
    team_members: List[User]

    @root_validator
    def check_dates(cls, values):
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise BusinessLogicError('Start date must be before end date')
        return values

# 4. Function to demonstrate error handling and propagation
def create_employee_project(employee_data: Dict, project_data: Dict):
    try:
        # Attempt to create an Employee instance
        employee = Employee(**employee_data)
        
        # Attempt to create a Project instance
        project = Project(**project_data)
        
        # If both succeed, return them
        return employee, project
    
    except ValidationError as e:
        print("Validation Error Occurred:")
        print(e.json())  # Print the validation error in JSON format
        
        # You can also access specific error details
        for error in e.errors():
            print(f"Error on field: {error['loc']}")
            print(f"Error type: {error['type']}")
            print(f"Error message: {error['msg']}")
        
        # Optionally, re-raise the exception or handle it as needed
        raise
    
    except BusinessLogicError as e:
        print(f"Business Logic Error: {str(e)}")
        # Handle or re-raise as needed
        raise
    
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        # Handle or re-raise as needed
        raise

# 5. Examples demonstrating various error scenarios
def run_examples():
    print("Example 1: Valid data")
    try:
        employee_data = {
            "user": {
                "id": 1,
                "username": "johndoe",
                "email": "john@company.com",
                "age": 30
            },
            "department": "IT",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "country": "USA",
                "postal_code": "12345"
            },
            "hire_date": "2023-01-15"
        }
        project_data = {
            "name": "Project Alpha",
            "start_date": "2023-02-01",
            "end_date": "2023-12-31",
            "budget": 100000.00,
            "team_members": [employee_data["user"]]
        }
        employee, project = create_employee_project(employee_data, project_data)
        print("Employee and Project created successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

    print("\nExample 2: Invalid User data (username)")
    try:
        invalid_employee_data = employee_data.copy()
        invalid_employee_data["user"]["username"] = "john@doe"  # Invalid username
        create_employee_project(invalid_employee_data, project_data)
    except Exception as e:
        print(f"Error: {str(e)}")

    print("\nExample 3: Invalid Email")
    try:
        invalid_employee_data = employee_data.copy()
        invalid_employee_data["user"]["email"] = "john@gmail.com"  # Not a company email
        create_employee_project(invalid_employee_data, project_data)
    except Exception as e:
        print(f"Error: {str(e)}")

    print("\nExample 4: Invalid Age")
    try:
        invalid_employee_data = employee_data.copy()
        invalid_employee_data["user"]["age"] = 15  # Below minimum age
        create_employee_project(invalid_employee_data, project_data)
    except Exception as e:
        print(f"Error: {str(e)}")

    print("\nExample 5: Invalid Project Dates")
    try:
        invalid_project_data = project_data.copy()
        invalid_project_data["start_date"] = "2023-12-31"
        invalid_project_data["end_date"] = "2023-01-01"
        create_employee_project(employee_data, invalid_project_data)
    except Exception as e:
        print(f"Error: {str(e)}")

    print("\nExample 6: Missing Required Field")
    try:
        invalid_employee_data = employee_data.copy()
        del invalid_employee_data["user"]["id"]  # Remove required field
        create_employee_project(invalid_employee_data, project_data)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_examples()
    
=====================================================
Basic Model with Validators:

The User model shows field-level and model-level validators.
It uses constrained types (constr, conint) for built-in validation.


Nested Model:

The Employee model demonstrates how errors in nested models (like User and Address) propagate up.


Custom Error Handling:

The Project model introduces a custom BusinessLogicError for domain-specific validation.


Error Handling Function:

create_employee_project shows how to handle different types of errors:

ValidationError: Pydantic's built-in error for data validation issues.
BusinessLogicError: Custom error for business logic violations.
General Exception catching for unexpected errors.




Multiple Examples:

The run_examples function demonstrates various error scenarios:

Valid data (success case)
Invalid username (fails username_alphanumeric validator)
Invalid email (fails check_email_domain validator)
Invalid age (fails conint constraint)
Invalid project dates (raises BusinessLogicError)
Missing required field (fails Pydantic's built-in required field check)





Key Points on Error Handling and Propagation:

ValidationError:

Pydantic raises this for any field that fails validation.
It contains detailed information about all validation errors.
You can access individual error details (field, error type, message).


Custom Errors:

You can raise custom exceptions (like BusinessLogicError) in validators.
These propagate up and can be caught separately from ValidationError.


Nested Model Errors:

Errors in nested models (like User within Employee) are included in the parent model's ValidationError.


Error Presentation:

Pydantic's ValidationError can be easily converted to JSON for API responses.


Granular Error Handling:

You can catch ValidationError separately from other exceptions for more specific error handling.


Root Validators:

Allow for model-wide validation and can raise both ValueError (caught by Pydantic) or custom exceptions.



This example provides a comprehensive overview of how Pydantic handles errors, how they propagate through nested models, and how you can implement custom error handling and business logic validation. It's particularly useful for building robust APIs or data processing pipelines where detailed error reporting is crucial.
