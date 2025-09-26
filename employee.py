#!/usr/bin/env python3
"""
Employee Management System - Model Layer
Employee class with validation, inheritance, and polymorphism
"""

import re
import logging
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('employee_test.log'),
        logging.StreamHandler()
    ]
)

class Employee:
    """Base Employee class with validation and properties"""
    
    def __init__(self, emp_id: str, fname: str, lname: str, department: str, ph_number: str, salary: float = 0.0):
        """Initialize employee with validation"""
        self._id = emp_id
        self.fname = fname
        self.lname = lname
        self.department = department
        self.ph_number = ph_number
        self.salary = salary
    
    @property
    def id(self) -> str:
        """Read-only employee ID"""
        return self._id
    
    @property
    def fname(self) -> str:
        """First name property with validation"""
        return self._fname
    
    @fname.setter
    def fname(self, value: str):
        """Set first name with validation"""
        if not value or not isinstance(value, str):
            raise ValueError("First name cannot be empty")
        if re.search(r'\d', value):
            raise ValueError("First name cannot contain digits")
        self._fname = value.strip().title()
    
    @property
    def lname(self) -> str:
        """Last name property with validation"""
        return self._lname
    
    @lname.setter
    def lname(self, value: str):
        """Set last name with validation"""
        if not value or not isinstance(value, str):
            raise ValueError("Last name cannot be empty")
        if re.search(r'\d', value):
            raise ValueError("Last name cannot contain digits")
        self._lname = value.strip().title()
    
    @property
    def department(self) -> str:
        """Department property with validation"""
        return self._department
    
    @department.setter
    def department(self, value: str):
        """Set department with validation"""
        if not value or not isinstance(value, str):
            raise ValueError("Department cannot be empty")
        if not re.match(r'^[A-Z]{2,3}$', value.upper()):
            raise ValueError("Department must be 2-3 uppercase letters")
        self._department = value.upper()
    
    @property
    def ph_number(self) -> str:
        """Phone number property"""
        return self._ph_number
    
    @ph_number.setter
    def ph_number(self, value: str):
        """Set phone number with sanitization"""
        if not value or not isinstance(value, str):
            raise ValueError("Phone number cannot be empty")
        
        # Sanitize phone number - remove all non-digits
        sanitized = re.sub(r'\D', '', value)
        
        if len(sanitized) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        
        self._ph_number = sanitized
    
    @property
    def salary(self) -> float:
        """Salary property with validation"""
        return self._salary
    
    @salary.setter
    def salary(self, value: float):
        """Set salary with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = float(value)
    
    def getphNumber(self) -> str:
        """Return unformatted 10-digit phone number"""
        return self._ph_number
    
    def get_formatted_phone(self) -> str:
        """Return formatted phone number for display"""
        return f"({self._ph_number[:3]})-{self._ph_number[3:6]}-{self._ph_number[6:]}"
    
    def __str__(self) -> str:
        """String representation of employee"""
        return (f"Employee ID: {self._id}, Name: {self._fname} {self._lname}, "
                f"Department: {self._department}, Phone: {self.get_formatted_phone()}, "
                f"Salary: ${self._salary:,.2f}")
    
    def to_dict(self) -> dict:
        """Convert employee to dictionary for CSV storage"""
        return {
            'id': self._id,
            'fname': self._fname,
            'lname': self._lname,
            'department': self._department,
            'ph_number': self._ph_number,
            'salary': self._salary,
            'employee_type': 'Employee'
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create employee from dictionary"""
        return cls(
            emp_id=data['id'],
            fname=data['fname'],
            lname=data['lname'],
            department=data['department'],
            ph_number=data['ph_number'],
            salary=float(data.get('salary', 0))
        )


class Manager(Employee):
    """Manager subclass with additional attributes"""
    
    def __init__(self, emp_id: str, fname: str, lname: str, department: str, 
                 ph_number: str, salary: float = 0.0, team_size: int = 0, office_number: str = ""):
        """Initialize manager with additional attributes"""
        super().__init__(emp_id, fname, lname, department, ph_number, salary)
        self.team_size = team_size
        self.office_number = office_number
    
    @property
    def team_size(self) -> int:
        """Team size property"""
        return self._team_size
    
    @team_size.setter
    def team_size(self, value: int):
        """Set team size with validation"""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Team size must be a non-negative integer")
        self._team_size = value
    
    @property
    def office_number(self) -> str:
        """Office number property"""
        return self._office_number
    
    @office_number.setter
    def office_number(self, value: str):
        """Set office number"""
        self._office_number = str(value) if value else ""
    
    def __str__(self) -> str:
        """String representation of manager (polymorphism)"""
        base_info = super().__str__()
        return (f"Manager - {base_info}, Team Size: {self._team_size}, "
                f"Office: {self._office_number}")
    
    def to_dict(self) -> dict:
        """Convert manager to dictionary for CSV storage"""
        data = super().to_dict()
        data.update({
            'employee_type': 'Manager',
            'team_size': self._team_size,
            'office_number': self._office_number
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create manager from dictionary"""
        return cls(
            emp_id=data['id'],
            fname=data['fname'],
            lname=data['lname'],
            department=data['department'],
            ph_number=data['ph_number'],
            salary=float(data.get('salary', 0)),
            team_size=data.get('team_size', 0),
            office_number=data.get('office_number', '')
        )


def test_employee_creation():
    """Test function to demonstrate employee creation and validation"""
    print("=== Testing Employee Creation ===")
    
    # Test valid employee creation
    try:
        emp1 = Employee("EMP001", "John", "Doe", "HR", "(555)-123-4567", 50000.0)
        print(f"✓ Created valid employee: {emp1}")
        logging.info(f"Successfully created employee: {emp1}")
    except ValueError as e:
        print(f"✗ Error creating employee: {e}")
        logging.error(f"Failed to create employee: {e}")
    
    # Test valid manager creation
    try:
        mgr1 = Manager("MGR001", "Jane", "Smith", "IT", "5559876543", 75000.0, 5, "A-101")
        print(f"✓ Created valid manager: {mgr1}")
        logging.info(f"Successfully created manager: {mgr1}")
    except ValueError as e:
        print(f"✗ Error creating manager: {e}")
        logging.error(f"Failed to create manager: {e}")
    
    # Test invalid employee creation (name with digits)
    try:
        emp2 = Employee("EMP002", "John2", "Doe", "HR", "5551234567", 45000.0)
        print(f"✗ Should have failed: {emp2}")
    except ValueError as e:
        print(f"✓ Correctly caught validation error: {e}")
        logging.error(f"Validation error caught: {e}")
    
    # Test invalid department
    try:
        emp3 = Employee("EMP003", "Alice", "Johnson", "HUMANRESOURCES", "5551234567", 50000.0)
        print(f"✗ Should have failed: {emp3}")
    except ValueError as e:
        print(f"✓ Correctly caught validation error: {e}")
        logging.error(f"Validation error caught: {e}")
    
    # Test invalid phone number
    try:
        emp4 = Employee("EMP004", "Bob", "Wilson", "IT", "123", 55000.0)
        print(f"✗ Should have failed: {emp4}")
    except ValueError as e:
        print(f"✓ Correctly caught validation error: {e}")
        logging.error(f"Validation error caught: {e}")
    
    # Test invalid salary
    try:
        emp5 = Employee("EMP005", "Carol", "Brown", "FIN", "5551234567", -1000.0)
        print(f"✗ Should have failed: {emp5}")
    except ValueError as e:
        print(f"✓ Correctly caught validation error: {e}")
        logging.error(f"Validation error caught: {e}")
    
    # Test phone number sanitization
    try:
        emp6 = Employee("EMP006", "David", "Lee", "IT", "555.123.4567", 60000.0)
        print(f"✓ Phone sanitization works: {emp6.get_formatted_phone()}")
        logging.info(f"Phone sanitization successful: {emp6.get_formatted_phone()}")
    except ValueError as e:
        print(f"✗ Phone sanitization failed: {e}")
        logging.error(f"Phone sanitization failed: {e}")


if __name__ == "__main__":
    test_employee_creation()
