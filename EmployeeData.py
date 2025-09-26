#!/usr/bin/env python3
"""
Employee Management System - Data Layer
Handles CSV file operations for employee data persistence
"""

import csv
import os
import logging
from typing import List, Dict, Any, Optional
from employee import Employee, Manager

# Configure logging for data operations
data_logger = logging.getLogger('data_operations')
data_logger.setLevel(logging.INFO)

class EmployeeData:
    """Data access layer for employee operations"""
    
    def __init__(self, csv_file: str = "employee_data.csv"):
        """Initialize with CSV file path"""
        self.csv_file = csv_file
        self.ensure_csv_exists()
    
    def ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'fname', 'lname', 'department', 'ph_number', 
                               'employee_type', 'team_size', 'office_number'])
            data_logger.info(f"Created new CSV file: {self.csv_file}")
    
    def load_employees(self) -> List[Employee]:
        """Load employees from CSV file"""
        employees = []
        
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        if row['employee_type'] == 'Manager':
                            employee = Manager.from_dict(row)
                        else:
                            employee = Employee.from_dict(row)
                        employees.append(employee)
                        data_logger.info(f"Loaded employee: {employee.id}")
                    except Exception as e:
                        data_logger.error(f"Error loading employee from row {row}: {e}")
                        continue
            
            data_logger.info(f"Successfully loaded {len(employees)} employees")
            return employees
            
        except FileNotFoundError:
            data_logger.error(f"CSV file not found: {self.csv_file}")
            return []
        except Exception as e:
            data_logger.error(f"Error loading employees: {e}")
            return []
    
    def save_employees(self, employees: List[Employee]) -> bool:
        """Save employees to CSV file"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                if not employees:
                    # Write headers even if no data
                    writer = csv.writer(file)
                    writer.writerow(['id', 'fname', 'lname', 'department', 'ph_number', 
                                   'employee_type', 'team_size', 'office_number'])
                    return True
                
                fieldnames = ['id', 'fname', 'lname', 'department', 'ph_number', 
                             'employee_type', 'team_size', 'office_number']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for employee in employees:
                    writer.writerow(employee.to_dict())
                    data_logger.info(f"Saved employee: {employee.id}")
            
            data_logger.info(f"Successfully saved {len(employees)} employees")
            return True
            
        except Exception as e:
            data_logger.error(f"Error saving employees: {e}")
            return False
    
    def add_employee(self, employee: Employee) -> bool:
        """Add a single employee to the CSV file"""
        employees = self.load_employees()
        
        # Check if employee ID already exists
        if any(emp.id == employee.id for emp in employees):
            data_logger.warning(f"Employee ID {employee.id} already exists")
            return False
        
        employees.append(employee)
        return self.save_employees(employees)
    
    def update_employee(self, employee_id: str, updated_employee: Employee) -> bool:
        """Update an existing employee"""
        employees = self.load_employees()
        
        for i, emp in enumerate(employees):
            if emp.id == employee_id:
                employees[i] = updated_employee
                data_logger.info(f"Updated employee: {employee_id}")
                return self.save_employees(employees)
        
        data_logger.warning(f"Employee ID {employee_id} not found for update")
        return False
    
    def delete_employee(self, employee_id: str) -> bool:
        """Delete an employee by ID"""
        employees = self.load_employees()
        
        original_count = len(employees)
        employees = [emp for emp in employees if emp.id != employee_id]
        
        if len(employees) < original_count:
            data_logger.info(f"Deleted employee: {employee_id}")
            return self.save_employees(employees)
        else:
            data_logger.warning(f"Employee ID {employee_id} not found for deletion")
            return False
    
    def find_employee(self, employee_id: str) -> Optional[Employee]:
        """Find an employee by ID"""
        employees = self.load_employees()
        
        for employee in employees:
            if employee.id == employee_id:
                return employee
        
        return None
    
    def get_employees_by_department(self, department: str) -> List[Employee]:
        """Get all employees in a specific department"""
        employees = self.load_employees()
        return [emp for emp in employees if emp.department == department.upper()]
    
    def get_employee_count(self) -> int:
        """Get total number of employees"""
        employees = self.load_employees()
        return len(employees)
    
    def backup_data(self, backup_file: str = None) -> bool:
        """Create a backup of the current data"""
        if backup_file is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"employee_data_backup_{timestamp}.csv"
        
        try:
            employees = self.load_employees()
            with open(backup_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'fname', 'lname', 'department', 'ph_number', 
                             'employee_type', 'team_size', 'office_number']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for employee in employees:
                    writer.writerow(employee.to_dict())
            
            data_logger.info(f"Created backup: {backup_file}")
            return True
            
        except Exception as e:
            data_logger.error(f"Error creating backup: {e}")
            return False


def test_data_operations():
    """Test function for data operations"""
    print("=== Testing Data Operations ===")
    
    # Create test employees
    emp1 = Employee("TEST001", "Test", "User", "IT", "5551234567")
    mgr1 = Manager("TEST002", "Test", "Manager", "HR", "5559876543", 3, "B-201")
    
    # Test data operations
    data_layer = EmployeeData("test_employees.csv")
    
    # Test adding employees
    print(f"Adding employee: {data_layer.add_employee(emp1)}")
    print(f"Adding manager: {data_layer.add_employee(mgr1)}")
    
    # Test loading employees
    employees = data_layer.load_employees()
    print(f"Loaded {len(employees)} employees:")
    for emp in employees:
        print(f"  - {emp}")
    
    # Test finding employee
    found = data_layer.find_employee("TEST001")
    print(f"Found employee: {found}")
    
    # Test updating employee
    emp1.fname = "Updated"
    print(f"Updated employee: {data_layer.update_employee('TEST001', emp1)}")
    
    # Test deleting employee
    print(f"Deleted employee: {data_layer.delete_employee('TEST001')}")
    
    # Clean up test file
    if os.path.exists("test_employees.csv"):
        os.remove("test_employees.csv")
        print("Cleaned up test file")


if __name__ == "__main__":
    test_data_operations()
