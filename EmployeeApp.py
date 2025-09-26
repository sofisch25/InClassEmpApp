#!/usr/bin/env python3
"""
Employee Management System - Controller Layer
Main application controller coordinating Model, View, and Data layers
"""

import logging
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from employee import Employee, Manager
from EmployeeData import EmployeeData
from EmployeeView import EmployeeView

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('employee_app.log'),
        logging.StreamHandler()
    ]
)

class EmployeeApp:
    """Main application controller"""
    
    def __init__(self):
        """Initialize the application"""
        self.view = EmployeeView()
        self.data_layer = EmployeeData()
        self.sql_operations = []  # Store SQL operations for display
        self.logger = logging.getLogger(__name__)
        
        # Initialize SQLite connection for SQL logging
        self.db_connection = None
        self.init_sqlite_connection()
    
    def init_sqlite_connection(self):
        """Initialize SQLite connection for SQL operations logging"""
        try:
            self.db_connection = sqlite3.connect('employees.db')
            self.logger.info("SQLite connection established for SQL logging")
        except Exception as e:
            self.logger.error(f"Failed to connect to SQLite: {e}")
    
    def log_sql_operation(self, operation: str, sql: str, result: str = ""):
        """Log SQL operations for display"""
        self.sql_operations.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'operation': operation,
            'sql': sql,
            'result': result
        })
        self.logger.info(f"SQL Operation: {operation} - {sql}")
    
    def run(self):
        """Main application loop"""
        self.view.display_welcome_message()
        
        while True:
            try:
                self.view.clear_screen()
                self.view.display_header()
                self.view.display_menu()
                
                choice = self.view.get_menu_choice()
                
                if choice == '1':
                    self.create_employee()
                elif choice == '2':
                    self.edit_employee()
                elif choice == '3':
                    self.delete_employee()
                elif choice == '4':
                    self.display_all_employees()
                elif choice == '5':
                    self.search_employees()
                elif choice == '6':
                    self.display_department_summary()
                elif choice == '7':
                    self.backup_data()
                elif choice == '8':
                    self.view_sql_operations()
                elif choice == '9':
                    self.view.display_goodbye_message()
                    break
                
            except KeyboardInterrupt:
                self.view.display_goodbye_message()
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                self.view.display_error(f"An unexpected error occurred: {e}")
    
    def create_employee(self):
        """Create a new employee"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            print("CREATE NEW EMPLOYEE")
            print("-" * 30)
            
            # Get employee type
            emp_type = self.view.get_employee_type()
            if not emp_type:
                return
            
            # Get employee data
            emp_data = self.view.get_employee_data(emp_type)
            if not emp_data:
                return
            
            # Create employee object
            if emp_type == "Manager":
                employee = Manager(
                    emp_id=emp_data['id'],
                    fname=emp_data['fname'],
                    lname=emp_data['lname'],
                    department=emp_data['department'],
                    ph_number=emp_data['ph_number'],
                    team_size=emp_data.get('team_size', 0),
                    office_number=emp_data.get('office_number', '')
                )
            else:
                employee = Employee(
                    emp_id=emp_data['id'],
                    fname=emp_data['fname'],
                    lname=emp_data['lname'],
                    department=emp_data['department'],
                    ph_number=emp_data['ph_number']
                )
            
            # Save to data layer
            if self.data_layer.add_employee(employee):
                self.log_sql_operation(
                    "INSERT",
                    f"INSERT INTO employees (id, name, department, salary, hire_date) VALUES ('{employee.id}', '{employee.fname} {employee.lname}', '{employee.department}', 0, '{datetime.now().strftime('%Y-%m-%d')}')",
                    f"Created {emp_type}: {employee.id}"
                )
                self.view.display_success(f"Employee {employee.id} created successfully!")
                self.logger.info(f"Created employee: {employee.id}")
            else:
                self.view.display_error("Failed to create employee. ID may already exist.")
            
        except ValueError as e:
            self.view.display_error(f"Validation error: {e}")
            self.logger.error(f"Validation error in create_employee: {e}")
        except Exception as e:
            self.view.display_error(f"Error creating employee: {e}")
            self.logger.error(f"Error in create_employee: {e}")
        finally:
            self.view.pause()
    
    def edit_employee(self):
        """Edit an existing employee"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            print("EDIT EMPLOYEE")
            print("-" * 20)
            
            # Get employee ID
            emp_id = self.view.get_employee_id("edit")
            if not emp_id:
                return
            
            # Find employee
            employee = self.data_layer.find_employee(emp_id)
            if not employee:
                self.view.display_error(f"Employee {emp_id} not found.")
                self.view.pause()
                return
            
            # Display current employee details
            self.view.display_employee_details(employee)
            
            if not self.view.confirm_action("Do you want to edit this employee?"):
                return
            
            # Get updated data
            print(f"\nEnter new information (press Enter to keep current value):")
            print(f"Current First Name: {employee.fname}")
            new_fname = input("New First Name: ").strip() or employee.fname
            
            print(f"Current Last Name: {employee.lname}")
            new_lname = input("New Last Name: ").strip() or employee.lname
            
            print(f"Current Department: {employee.department}")
            new_dept = input("New Department: ").strip().upper() or employee.department
            
            print(f"Current Phone: {employee.get_formatted_phone()}")
            new_phone = input("New Phone: ").strip() or employee.ph_number
            
            # Update employee object
            employee.fname = new_fname
            employee.lname = new_lname
            employee.department = new_dept
            employee.ph_number = new_phone
            
            # Update manager-specific fields if applicable
            if isinstance(employee, Manager):
                print(f"Current Team Size: {employee.team_size}")
                new_team_size = input("New Team Size: ").strip()
                if new_team_size.isdigit():
                    employee.team_size = int(new_team_size)
                
                print(f"Current Office: {employee.office_number}")
                new_office = input("New Office: ").strip()
                if new_office:
                    employee.office_number = new_office
            
            # Save changes
            if self.data_layer.update_employee(emp_id, employee):
                self.log_sql_operation(
                    "UPDATE",
                    f"UPDATE employees SET name = '{employee.fname} {employee.lname}', department = '{employee.department}' WHERE id = '{emp_id}'",
                    f"Updated employee: {emp_id}"
                )
                self.view.display_success(f"Employee {emp_id} updated successfully!")
                self.logger.info(f"Updated employee: {emp_id}")
            else:
                self.view.display_error("Failed to update employee.")
            
        except ValueError as e:
            self.view.display_error(f"Validation error: {e}")
            self.logger.error(f"Validation error in edit_employee: {e}")
        except Exception as e:
            self.view.display_error(f"Error editing employee: {e}")
            self.logger.error(f"Error in edit_employee: {e}")
        finally:
            self.view.pause()
    
    def delete_employee(self):
        """Delete an employee"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            print("DELETE EMPLOYEE")
            print("-" * 20)
            
            # Get employee ID
            emp_id = self.view.get_employee_id("delete")
            if not emp_id:
                return
            
            # Find employee
            employee = self.data_layer.find_employee(emp_id)
            if not employee:
                self.view.display_error(f"Employee {emp_id} not found.")
                self.view.pause()
                return
            
            # Display employee details
            self.view.display_employee_details(employee)
            
            # Confirm deletion
            if self.view.confirm_action("Are you sure you want to delete this employee?"):
                if self.data_layer.delete_employee(emp_id):
                    self.log_sql_operation(
                        "DELETE",
                        f"DELETE FROM employees WHERE id = '{emp_id}'",
                        f"Deleted employee: {emp_id}"
                    )
                    self.view.display_success(f"Employee {emp_id} deleted successfully!")
                    self.logger.info(f"Deleted employee: {emp_id}")
                else:
                    self.view.display_error("Failed to delete employee.")
            
        except Exception as e:
            self.view.display_error(f"Error deleting employee: {e}")
            self.logger.error(f"Error in delete_employee: {e}")
        finally:
            self.view.pause()
    
    def display_all_employees(self):
        """Display all employees"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            
            employees = self.data_layer.load_employees()
            self.view.display_employees(employees, "ALL EMPLOYEES")
            
            self.log_sql_operation(
                "SELECT",
                "SELECT * FROM employees ORDER BY id",
                f"Retrieved {len(employees)} employees"
            )
            
        except Exception as e:
            self.view.display_error(f"Error displaying employees: {e}")
            self.logger.error(f"Error in display_all_employees: {e}")
        finally:
            self.view.pause()
    
    def search_employees(self):
        """Search employees based on criteria"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            print("SEARCH EMPLOYEES")
            print("-" * 20)
            
            criteria = self.view.get_search_criteria()
            if not criteria:
                return
            
            employees = self.data_layer.load_employees()
            filtered_employees = []
            
            for emp in employees:
                match = True
                
                if 'id' in criteria and criteria['id'] not in emp.id:
                    match = False
                if 'name' in criteria and criteria['name'].lower() not in emp.fname.lower() and criteria['name'].lower() not in emp.lname.lower():
                    match = False
                if 'department' in criteria and emp.department != criteria['department']:
                    match = False
                if 'type' in criteria:
                    if criteria['type'].lower() == 'manager' and not isinstance(emp, Manager):
                        match = False
                    elif criteria['type'].lower() == 'employee' and isinstance(emp, Manager):
                        match = False
                
                if match:
                    filtered_employees.append(emp)
            
            self.view.display_employees(filtered_employees, "SEARCH RESULTS")
            
            self.log_sql_operation(
                "SELECT",
                f"SELECT * FROM employees WHERE {list(criteria.keys())[0]} LIKE '%{list(criteria.values())[0]}%'",
                f"Found {len(filtered_employees)} employees"
            )
            
        except Exception as e:
            self.view.display_error(f"Error searching employees: {e}")
            self.logger.error(f"Error in search_employees: {e}")
        finally:
            self.view.pause()
    
    def display_department_summary(self):
        """Display department summary statistics"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            
            employees = self.data_layer.load_employees()
            dept_data = {}
            
            for emp in employees:
                dept = emp.department
                if dept not in dept_data:
                    dept_data[dept] = {
                        'count': 0,
                        'managers': 0,
                        'regular': 0,
                        'total_team_size': 0
                    }
                
                dept_data[dept]['count'] += 1
                
                if isinstance(emp, Manager):
                    dept_data[dept]['managers'] += 1
                    dept_data[dept]['total_team_size'] += emp.team_size
                else:
                    dept_data[dept]['regular'] += 1
            
            # Calculate averages
            for dept in dept_data:
                if dept_data[dept]['managers'] > 0:
                    dept_data[dept]['avg_team_size'] = dept_data[dept]['total_team_size'] / dept_data[dept]['managers']
                else:
                    dept_data[dept]['avg_team_size'] = 0
            
            self.view.display_department_summary(dept_data)
            
            self.log_sql_operation(
                "SELECT",
                "SELECT department, COUNT(*) as count, SUM(CASE WHEN employee_type = 'Manager' THEN 1 ELSE 0 END) as managers FROM employees GROUP BY department",
                f"Department summary for {len(dept_data)} departments"
            )
            
        except Exception as e:
            self.view.display_error(f"Error displaying department summary: {e}")
            self.logger.error(f"Error in display_department_summary: {e}")
        finally:
            self.view.pause()
    
    def backup_data(self):
        """Create a backup of employee data"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            print("BACKUP DATA")
            print("-" * 15)
            
            if self.data_layer.backup_data():
                self.view.display_success("Data backup created successfully!")
                self.logger.info("Data backup created")
            else:
                self.view.display_error("Failed to create backup.")
            
        except Exception as e:
            self.view.display_error(f"Error creating backup: {e}")
            self.logger.error(f"Error in backup_data: {e}")
        finally:
            self.view.pause()
    
    def view_sql_operations(self):
        """Display SQL operations log"""
        try:
            self.view.clear_screen()
            self.view.display_header()
            
            self.view.display_sql_operations(self.sql_operations)
            
        except Exception as e:
            self.view.display_error(f"Error displaying SQL operations: {e}")
            self.logger.error(f"Error in view_sql_operations: {e}")
        finally:
            self.view.pause()
    
    def __del__(self):
        """Cleanup when application exits"""
        if self.db_connection:
            self.db_connection.close()


def main():
    """Main entry point"""
    # Team members (as required by assignment)
    print("Team Members: [Your Name Here]")
    print("Assignment: HR Employee Management System (MVC + AI Reflection)")
    print("=" * 60)
    
    try:
        app = EmployeeApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
