# handling error - 02
import logging
from pydantic import BaseModel, ValidationError, validator, root_validator, constr, conint, EmailStr
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import json
import traceback
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Custom exceptions
class BusinessLogicError(Exception):
    """Custom exception for business logic violations."""
    pass

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

# Pydantic models
class User(BaseModel):
    id: int
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    age: conint(ge=18, le=120)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @root_validator
    def check_email_domain(cls, values):
        email = values.get('email')
        if email and not email.endswith('@company.com'):
            raise ValueError('Email must be a company email')
        return values

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

# Error handling decorator
def handle_errors(func):
    """
    A decorator to handle errors in a consistent manner.
    It logs errors, formats them for the caller, and re-raises when necessary.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            # Log the full error details
            logger.error(f"Validation error in {func.__name__}: {e.json()}")
            # Format error for the caller
            formatted_errors = [
                {
                    "field": ".".join(map(str, error["loc"])),
                    "error": error["msg"]
                }
                for error in e.errors()
            ]
            # Re-raise a custom exception with formatted errors
            raise ValueError(json.dumps(formatted_errors))
        except BusinessLogicError as e:
            # Log the business logic error
            logger.error(f"Business logic error in {func.__name__}: {str(e)}")
            # Re-raise the error as is
            raise
        except DatabaseError as e:
            # Log the database error
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            # Re-raise a generic error to hide implementation details
            raise Exception("An internal error occurred. Please try again later.")
        except Exception as e:
            # Log unexpected errors with full traceback
            logger.critical(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
            # Re-raise a generic error
            raise Exception("An unexpected error occurred. Please contact support.")
    return wrapper

# Mock database functions
def save_to_database(data: Dict[str, Any]) -> None:
    """Mock function to simulate saving data to a database."""
    # Simulate a database error for demonstration
    if "error" in data:
        raise DatabaseError("Failed to save to database")
    logger.info(f"Saved to database: {data}")

def get_from_database(id: int) -> Dict[str, Any]:
    """Mock function to simulate retrieving data from a database."""
    # Simulate data retrieval
    return {"id": id, "name": "Sample Data"}

# Main function to create employee and project
@handle_errors
def create_employee_project(employee_data: Dict[str, Any], project_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates an employee and a project, demonstrating error handling and logging.
    
    Args:
        employee_data (Dict[str, Any]): Dictionary containing employee data
        project_data (Dict[str, Any]): Dictionary containing project data
    
    Returns:
        Dict[str, Any]: Dictionary containing created employee and project data
    
    Raises:
        ValueError: If there are validation errors in the input data
        BusinessLogicError: If there are business logic violations
        Exception: For other unexpected errors
    """
    logger.info("Attempting to create employee and project")
    
    # Create Employee instance
    employee = Employee(**employee_data)
    logger.debug(f"Employee instance created: {employee}")

    # Create Project instance
    project = Project(**project_data)
    logger.debug(f"Project instance created: {project}")

    # Simulate saving to database
    try:
        save_to_database(employee.dict())
        save_to_database(project.dict())
    except DatabaseError as e:
        logger.error(f"Failed to save to database: {str(e)}")
        raise

    logger.info("Employee and project created successfully")
    return {
        "employee": employee.dict(),
        "project": project.dict()
    }

# Function to demonstrate error handling
def run_examples():
    examples = [
        {
            "name": "Valid data",
            "employee_data": {
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
            },
            "project_data": {
                "name": "Project Alpha",
                "start_date": "2023-02-01",
                "end_date": "2023-12-31",
                "budget": 100000.00,
                "team_members": [
                    {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@company.com",
                        "age": 30
                    }
                ]
            }
        },
        {
            "name": "Invalid username",
            "employee_data": {
                "user": {
                    "id": 2,
                    "username": "jane@doe",  # Invalid username
                    "email": "jane@company.com",
                    "age": 28
                },
                "department": "HR",
                "address": {
                    "street": "456 Elm St",
                    "city": "Other City",
                    "country": "Canada",
                    "postal_code": "A1B 2C3"
                },
                "hire_date": "2023-02-01"
            },
            "project_data": {
                "name": "Project Beta",
                "start_date": "2023-03-01",
                "end_date": "2023-11-30",
                "budget": 75000.00,
                "team_members": [
                    {
                        "id": 2,
                        "username": "jane@doe",
                        "email": "jane@company.com",
                        "age": 28
                    }
                ]
            }
        },
        {
            "name": "Invalid project dates",
            "employee_data": {
                "user": {
                    "id": 3,
                    "username": "bobsmith",
                    "email": "bob@company.com",
                    "age": 35
                },
                "department": "Sales",
                "address": {
                    "street": "789 Oak Rd",
                    "city": "Somewhere",
                    "country": "UK",
                    "postal_code": "SW1A 1AA"
                },
                "hire_date": "2023-03-15"
            },
            "project_data": {
                "name": "Project Gamma",
                "start_date": "2023-12-31",  # Start date after end date
                "end_date": "2023-01-01",
                "budget": 50000.00,
                "team_members": [
                    {
                        "id": 3,
                        "username": "bobsmith",
                        "email": "bob@company.com",
                        "age": 35
                    }
                ]
            }
        },
        {
            "name": "Database error",
            "employee_data": {
                "user": {
                    "id": 4,
                    "username": "alicejohnson",
                    "email": "alice@company.com",
                    "age": 40
                },
                "department": "Marketing",
                "address": {
                    "street": "101 Pine Lane",
                    "city": "Elsewhere",
                    "country": "Australia",
                    "postal_code": "2000"
                },
                "hire_date": "2023-04-01"
            },
            "project_data": {
                "name": "Project Delta",
                "start_date": "2023-05-01",
                "end_date": "2023-10-31",
                "budget": 120000.00,
                "team_members": [
                    {
                        "id": 4,
                        "username": "alicejohnson",
                        "email": "alice@company.com",
                        "age": 40
                    }
                ],
                "error": True  # This will trigger a simulated database error
            }
        }
    ]

    for example in examples:
        print(f"\nRunning example: {example['name']}")
        try:
            result = create_employee_project(example['employee_data'], example['project_data'])
            print("Success:", json.dumps(result, indent=2, default=str))
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_examples()
    
==================================================
This example provides a comprehensive demonstration of error handling, propagation, and logging. Here's a breakdown of the key components and concepts:

Logging Setup:

Configures logging with a specific format including timestamp, logger name, log level, and message.
Uses a module-level logger for consistent logging across the module.


Custom Exceptions:

BusinessLogicError: For domain-specific logic violations.
DatabaseError: To simulate database-related errors.


Pydantic Models:

Defines User, Address, Employee, and Project models with various validators.
Demonstrates nested models and complex validation rules.


Error Handling Decorator:

handle_errors decorator provides a centralized way to handle different types of errors.
It logs errors, formats them for the caller, and re-raises when necessary.
Demonstrates how to handle different exception types differently:

ValidationError: Logs details and re-raises with formatted error messages.
BusinessLogicError: Logs and re-raises as is.
DatabaseError: Logs and re-raises as a generic error to hide implementation details.
Unexpected errors: Logs full traceback and raises a generic error.




Mock Database Functions:

save_to_database and get_from_database simulate database operations.
save_to_database includes a simulated error scenario.


Main Function:

create_employee_project is decorated with @handle_errors.
Demonstrates proper logging at different stages of the process.
Shows how to handle potential database errors.


Example Runner:

run_examples function tests various scenarios:

Valid data
Invalid username (to trigger validation error)
Invalid project dates (to trigger business logic error)
Database error scenario




Error Propagation:

Errors are caught by the decorator and propagated to the caller with appropriate formatting.
Different types of errors are handled and logged differently.


Logging Best Practices:

Uses different log levels (INFO, DEBUG, ERROR, CRITICAL) appropriately.
Includes relevant context in log messages.
Logs full tracebacks for unexpected errors.


Error Formatting for API Responses:

Formats validation errors in a way that's suitable for API responses.



This example demonstrates a robust approach to error handling and logging that's suitable for production environments. It shows how to:

Use Pydantic for data validation
Implement custom business logic checks
Handle and log different types of errors consistently
Propagate errors to the caller in a controlled manner
Use logging effectively to aid in debugging and monitoring

By following these patterns, you can create more maintainable and debuggable applications, especially when dealing with complex data processing or API endpoints.
