from typing import List, Dict, Optional, ClassVar, Any
from pydantic import BaseModel, Field, validator, root_validator, PrivateAttr
from datetime import datetime, timedelta
import uuid

class Employee(BaseModel):
    """
    Represents an employee in the company.
    
    This model demonstrates the use of various Pydantic features along with
    OOP concepts like properties, class methods, and static methods.
    """
    
    # Class variable to keep track of all departments
    _departments: ClassVar[List[str]] = ["HR", "IT", "Finance", "Marketing"]
    
    # Instance fields
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: str
    department: str
    salary: float
    hire_date: datetime
    
    # Private attribute (not included in serialization)
    _total_paid: float = PrivateAttr(default=0.0)

    # Validators
    @validator('email')
    def email_must_be_company_email(cls, v):
        if not v.endswith('@company.com'):
            raise ValueError('Email must be a company email')
        return v

    @validator('department')
    def department_must_be_valid(cls, v):
        if v not in cls._departments:
            raise ValueError(f'Invalid department. Must be one of {cls._departments}')
        return v

    @root_validator
    def set_email_if_not_provided(cls, values):
        """Set email to name@company.com if not provided."""
        if 'email' not in values and 'name' in values:
            values['email'] = f"{values['name'].replace(' ', '').lower()}@company.com"
        return values

    # Properties
    @property
    def years_employed(self) -> float:
        """Calculate the number of years the employee has been with the company."""
        return (datetime.now() - self.hire_date).days / 365.25

    @property
    def total_paid(self) -> float:
        """Get the total amount paid to the employee."""
        return self._total_paid

    # Setter for total_paid
    @total_paid.setter
    def total_paid(self, value: float):
        """Set the total amount paid to the employee."""
        if value < self._total_paid:
            raise ValueError("Total paid can only increase")
        self._total_paid = value

    # Class methods
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """Create an Employee instance from a dictionary."""
        return cls(**data)

    @classmethod
    def add_department(cls, department: str) -> None:
        """Add a new department to the list of valid departments."""
        if department not in cls._departments:
            cls._departments.append(department)

    # Static methods
    @staticmethod
    def is_senior(years: float) -> bool:
        """Determine if an employee is considered senior based on years of employment."""
        return years >= 5

    # Instance methods
    def give_raise(self, amount: float) -> None:
        """Give the employee a raise."""
        self.salary += amount
        self.total_paid += amount

    def change_department(self, new_department: str) -> None:
        """Change the employee's department."""
        if new_department not in self._departments:
            raise ValueError(f'Invalid department. Must be one of {self._departments}')
        self.department = new_department

    def __str__(self) -> str:
        return f"{self.name} - {self.department}"

# Usage examples
if __name__ == "__main__":
    # Creating an employee
    john = Employee(
        name="John Doe",
        department="IT",
        salary=75000,
        hire_date=datetime(2018, 5, 15)
    )
    print(f"Employee created: {john}")
    print(f"John's email: {john.email}")  # Auto-generated email

    # Using properties
    print(f"Years employed: {john.years_employed:.2f}")
    print(f"Total paid: ${john.total_paid:.2f}")

    # Using instance methods
    john.give_raise(5000)
    print(f"New salary: ${john.salary:.2f}")
    print(f"New total paid: ${john.total_paid:.2f}")

    # Using static method
    print(f"Is John a senior employee? {Employee.is_senior(john.years_employed)}")

    # Using class method to add a new department
    Employee.add_department("Research")
    john.change_department("Research")
    print(f"John's new department: {john.department}")

    # Creating an employee from a dictionary
    jane_data = {
        "name": "Jane Smith",
        "email": "jane.smith@company.com",
        "department": "HR",
        "salary": 80000,
        "hire_date": datetime(2015, 3, 1)
    }
    jane = Employee.from_dict(jane_data)
    print(f"New employee created: {jane}")

    # Demonstrating validation
    try:
        Employee(
            name="Invalid Employee",
            email="invalid@gmail.com",  # This will raise a validation error
            department="IT",
            salary=70000,
            hire_date=datetime.now()
        )
    except ValueError as e:
        print(f"Validation error: {e}")

class Department(BaseModel):
    """
    Represents a department in the company.
    
    This model demonstrates the use of relationships between Pydantic models
    and more advanced OOP concepts.
    """
    
    name: str
    manager: Optional[Employee] = None
    employees: List[Employee] = Field(default_factory=list)
    budget: float
    
    # Class variable to store all departments
    _all_departments: ClassVar[Dict[str, 'Department']] = {}
    
    # Validators
    @validator('name')
    def name_must_be_valid(cls, v):
        if v not in Employee._departments:
            raise ValueError(f'Invalid department name. Must be one of {Employee._departments}')
        return v

    @root_validator
    def manager_must_be_in_department(cls, values):
        manager = values.get('manager')
        name = values.get('name')
        if manager and manager.department != name:
            raise ValueError('Manager must be in the same department')
        return values

    # Properties
    @property
    def total_salary(self) -> float:
        """Calculate the total salary for all employees in the department."""
        return sum(employee.salary for employee in self.employees)

    @property
    def average_salary(self) -> float:
        """Calculate the average salary for the department."""
        if not self.employees:
            return 0
        return self.total_salary / len(self.employees)

    # Class methods
    @classmethod
    def get_department(cls, name: str) -> 'Department':
        """Get a department by name, creating it if it doesn't exist."""
        if name not in cls._all_departments:
            cls._all_departments[name] = cls(name=name, budget=0)
        return cls._all_departments[name]

    # Instance methods
    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the department."""
        if employee.department != self.name:
            raise ValueError('Employee must be in this department')
        self.employees.append(employee)

    def remove_employee(self, employee: Employee) -> None:
        """Remove an employee from the department."""
        self.employees.remove(employee)

    def set_manager(self, employee: Employee) -> None:
        """Set the manager for the department."""
        if employee not in self.employees:
            raise ValueError('Manager must be an employee in the department')
        self.manager = employee

    def __str__(self) -> str:
        return f"{self.name} Department (Manager: {self.manager.name if self.manager else 'None'})"

# Usage examples for Department
if __name__ == "__main__":
    # Creating departments
    it_dept = Department.get_department("IT")
    hr_dept = Department.get_department("HR")

    # Adding employees to departments
    it_dept.add_employee(john)
    hr_dept.add_employee(jane)

    # Setting department budgets
    it_dept.budget = 1000000
    hr_dept.budget = 500000

    # Setting department managers
    it_dept.set_manager(john)
    hr_dept.set_manager(jane)

    print(f"IT Department: {it_dept}")
    print(f"HR Department: {hr_dept}")

    print(f"IT Department total salary: ${it_dept.total_salary:.2f}")
    print(f"HR Department average salary: ${hr_dept.average_salary:.2f}")

    # Demonstrating validation
    try:
        Department.get_department("Invalid")  # This will raise a validation error
    except ValueError as e:
        print(f"Validation error: {e}")
        
This extended example demonstrates:

Use of Pydantic models (Employee and Department) with various field types and validators.
Implementation of class variables (_departments in Employee, _all_departments in Department).
Use of properties for derived attributes (years_employed, total_salary, average_salary).
Implementation of class methods for alternative constructors and class-level operations (from_dict, add_department, get_department).
Use of static methods for utility functions (is_senior).
Implementation of instance methods for object-specific operations (give_raise, change_department, add_employee, remove_employee, set_manager).
Demonstration of relationships between models (Department containing Employee instances).
Use of private attributes with PrivateAttr and property setters.
Implementation of __str__ methods for custom string representations.
Extensive use of type hints for improved code clarity and IDE support.
Comprehensive validation logic using Pydantic's validators.
Demonstration of how to use these models and methods in practice.

This example showcases how Pydantic can be integrated with traditional OOP practices to create robust, self-validating data models with rich functionality. It combines the benefits of Pydantic's data validation with the structure and behavior capabilities of OOP.
