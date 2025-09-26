#!/usr/bin/env python3
"""
Employee Management System - View Layer
Handles all user interface and display operations
"""

import os
import sys
from typing import List, Optional, Dict, Any
from employee import Employee, Manager

class EmployeeView:
    """View class for handling all UI operations"""
    
    def __init__(self):
        """Initialize the view"""
        self.clear_screen()
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display application header"""
        print("=" * 60)
        print("           EMPLOYEE MANAGEMENT SYSTEM")
        print("=" * 60)
        print()
    
    def display_menu(self):
        """Display main menu options"""
        print("MAIN MENU:")
        print("1. Create New Employee")
        print("2. Edit Existing Employee")
        print("3. Delete Existing Employee")
        print("4. Display All Employees")
        print("5. Search Employees")
        print("6. Display Department Summary")
        print("7. Salary Analytics")
        print("8. Backup Data")
        print("9. View SQL Operations Log")
        print("10. Quit")
        print("-" * 40)
    
    def get_menu_choice(self) -> str:
        """Get user's menu choice"""
        while True:
            try:
                choice = input("Enter your choice (1-10): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                    return choice
                else:
                    self.display_error("Invalid choice. Please enter 1-10.")
            except KeyboardInterrupt:
                print("\nExiting...")
                return '10'
            except EOFError:
                print("\nExiting...")
                return '10'
    
    def get_employee_id(self, action: str) -> str:
        """Get employee ID from user"""
        while True:
            try:
                emp_id = input(f"Enter Employee ID to {action}: ").strip().upper()
                if emp_id:
                    return emp_id
                else:
                    self.display_error("Employee ID cannot be empty.")
            except KeyboardInterrupt:
                return ""
            except EOFError:
                return ""
    
    def get_employee_data(self, employee_type: str = "Employee") -> Dict[str, Any]:
        """Get employee data from user input"""
        data = {}
        
        # Get employee ID
        while True:
            try:
                emp_id = input("Enter Employee ID: ").strip().upper()
                if emp_id:
                    data['id'] = emp_id
                    break
                else:
                    self.display_error("Employee ID cannot be empty.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        # Get first name
        while True:
            try:
                fname = input("Enter First Name: ").strip()
                if fname:
                    data['fname'] = fname
                    break
                else:
                    self.display_error("First name cannot be empty.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        # Get last name
        while True:
            try:
                lname = input("Enter Last Name: ").strip()
                if lname:
                    data['lname'] = lname
                    break
                else:
                    self.display_error("Last name cannot be empty.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        # Get department
        while True:
            try:
                dept = input("Enter Department (3 letters, e.g., HR, IT, FIN): ").strip().upper()
                if dept:
                    data['department'] = dept
                    break
                else:
                    self.display_error("Department cannot be empty.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        # Get phone number
        while True:
            try:
                phone = input("Enter Phone Number (10 digits, any format): ").strip()
                if phone:
                    data['ph_number'] = phone
                    break
                else:
                    self.display_error("Phone number cannot be empty.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        # Get salary
        while True:
            try:
                salary_input = input("Enter Annual Salary: ").strip()
                if salary_input:
                    salary = float(salary_input)
                    if salary >= 0:
                        data['salary'] = salary
                        break
                    else:
                        self.display_error("Salary cannot be negative.")
                else:
                    self.display_error("Salary cannot be empty.")
            except ValueError:
                self.display_error("Please enter a valid number for salary.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        # Get manager-specific data
        if employee_type == "Manager":
            while True:
                try:
                    team_size = input("Enter Team Size (0 or more): ").strip()
                    if team_size.isdigit():
                        data['team_size'] = int(team_size)
                        break
                    else:
                        self.display_error("Team size must be a number.")
                except KeyboardInterrupt:
                    return {}
                except EOFError:
                    return {}
            
            try:
                office = input("Enter Office Number (optional): ").strip()
                data['office_number'] = office
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        return data
    
    def get_employee_type(self) -> str:
        """Get employee type from user"""
        while True:
            try:
                print("\nEmployee Type:")
                print("1. Regular Employee")
                print("2. Manager")
                choice = input("Select type (1-2): ").strip()
                
                if choice == '1':
                    return "Employee"
                elif choice == '2':
                    return "Manager"
                else:
                    self.display_error("Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                return "Employee"
            except EOFError:
                return "Employee"
    
    def display_employees(self, employees: List[Employee], title: str = "EMPLOYEES"):
        """Display list of employees"""
        if not employees:
            self.display_message("No employees found.")
            return
        
        print(f"\n{title}:")
        print("-" * 100)
        print(f"{'ID':<10} {'Name':<25} {'Department':<12} {'Phone':<15} {'Salary':<12} {'Type':<10}")
        print("-" * 100)
        
        for emp in employees:
            phone = emp.get_formatted_phone()
            emp_type = "Manager" if isinstance(emp, Manager) else "Employee"
            salary_str = f"${emp.salary:,.0f}"
            print(f"{emp.id:<10} {emp.fname + ' ' + emp.lname:<25} {emp.department:<12} {phone:<15} {salary_str:<12} {emp_type:<10}")
            
            # Show additional manager info
            if isinstance(emp, Manager):
                print(f"{'':>10} Team Size: {emp.team_size}, Office: {emp.office_number}")
        
        print("-" * 100)
        print(f"Total: {len(employees)} employees")
    
    def display_employee_details(self, employee: Employee):
        """Display detailed information about a single employee"""
        if not employee:
            self.display_error("Employee not found.")
            return
        
        print(f"\nEMPLOYEE DETAILS:")
        print("-" * 40)
        print(f"ID: {employee.id}")
        print(f"Name: {employee.fname} {employee.lname}")
        print(f"Department: {employee.department}")
        print(f"Phone: {employee.get_formatted_phone()}")
        print(f"Salary: ${employee.salary:,.2f}")
        print(f"Type: {'Manager' if isinstance(employee, Manager) else 'Employee'}")
        
        if isinstance(employee, Manager):
            print(f"Team Size: {employee.team_size}")
            print(f"Office: {employee.office_number}")
        
        print("-" * 40)
    
    def display_department_summary(self, department_data: Dict[str, Any]):
        """Display department summary statistics"""
        print(f"\nDEPARTMENT SUMMARY:")
        print("-" * 50)
        
        for dept, info in department_data.items():
            print(f"{dept}:")
            print(f"  Employees: {info['count']}")
            print(f"  Managers: {info['managers']}")
            print(f"  Regular: {info['regular']}")
            if info['count'] > 0:
                print(f"  Average Team Size: {info['avg_team_size']:.1f}")
            print()
    
    def display_sql_operations(self, operations: List[Dict[str, Any]]):
        """Display SQL operations log"""
        if not operations:
            self.display_message("No SQL operations logged.")
            return
        
        print(f"\nSQL OPERATIONS LOG:")
        print("-" * 60)
        
        for i, op in enumerate(operations, 1):
            print(f"{i}. {op['timestamp']} - {op['operation']}")
            print(f"   SQL: {op['sql']}")
            if op.get('result'):
                print(f"   Result: {op['result']}")
            print()
    
    def display_salary_analytics_menu(self):
        """Display salary analytics menu"""
        print("\nSALARY ANALYTICS MENU:")
        print("1. Overall Salary Statistics")
        print("2. Department Salary Breakdown")
        print("3. Employee Type Salary Comparison")
        print("4. Top 5 Highest Paid Employees")
        print("5. Top 5 Lowest Paid Employees")
        print("6. Salary Gap Analysis")
        print("7. Generate Complete Salary Report")
        print("8. View Recent Salary Changes")
        print("9. Back to Main Menu")
        print("-" * 40)
    
    def get_analytics_choice(self) -> str:
        """Get analytics menu choice"""
        while True:
            try:
                choice = input("Enter your choice (1-9): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return choice
                else:
                    self.display_error("Invalid choice. Please enter 1-9.")
            except KeyboardInterrupt:
                return '9'
            except EOFError:
                return '9'
    
    def display_salary_statistics(self, stats: Dict[str, Any]):
        """Display salary statistics"""
        print(f"\nSALARY STATISTICS:")
        print("-" * 30)
        print(f"Total Employees: {stats['count']}")
        print(f"Average Salary: ${stats['average']:,.2f}")
        print(f"Minimum Salary: ${stats['min']:,.2f}")
        print(f"Maximum Salary: ${stats['max']:,.2f}")
        print(f"Median Salary: ${stats['median']:,.2f}")
        print(f"Total Payroll: ${stats['total']:,.2f}")
    
    def display_department_salary_breakdown(self, dept_stats: Dict[str, Dict[str, Any]]):
        """Display department salary breakdown"""
        print(f"\nDEPARTMENT SALARY BREAKDOWN:")
        print("-" * 50)
        for dept, stats in dept_stats.items():
            print(f"{dept}:")
            print(f"  Count: {stats['count']}")
            print(f"  Average: ${stats['average']:,.2f}")
            print(f"  Range: ${stats['min']:,.2f} - ${stats['max']:,.2f}")
            print(f"  Total: ${stats['total']:,.2f}")
            print()
    
    def display_employee_type_comparison(self, type_stats: Dict[str, Dict[str, Any]]):
        """Display employee type salary comparison"""
        print(f"\nEMPLOYEE TYPE SALARY COMPARISON:")
        print("-" * 50)
        for emp_type, stats in type_stats.items():
            print(f"{emp_type}:")
            print(f"  Count: {stats['count']}")
            print(f"  Average: ${stats['average']:,.2f}")
            print(f"  Range: ${stats['min']:,.2f} - ${stats['max']:,.2f}")
            print(f"  Total: ${stats['total']:,.2f}")
            print()
    
    def display_top_earners(self, employees: List[Employee], title: str):
        """Display top earners"""
        print(f"\n{title}:")
        print("-" * 60)
        for i, emp in enumerate(employees, 1):
            emp_type = "Manager" if isinstance(emp, Manager) else "Employee"
            print(f"{i}. {emp.fname} {emp.lname} ({emp.department}) - ${emp.salary:,.2f} ({emp_type})")
    
    def display_salary_gap_analysis(self, gap_analysis: Dict[str, Any]):
        """Display salary gap analysis"""
        if 'error' in gap_analysis:
            print(f"\nError: {gap_analysis['error']}")
            return
        
        print(f"\nSALARY GAP ANALYSIS:")
        print("-" * 30)
        print(f"Regular Employee Average: ${gap_analysis['regular_employee_average']:,.2f}")
        print(f"Manager Average: ${gap_analysis['manager_average']:,.2f}")
        print(f"Absolute Gap: ${gap_analysis['absolute_gap']:,.2f}")
        print(f"Percentage Gap: {gap_analysis['percentage_gap']:.1f}%")
        print(f"Regular Employees: {gap_analysis['regular_count']}")
        print(f"Managers: {gap_analysis['manager_count']}")
    
    def display_salary_report(self, report: str):
        """Display complete salary report"""
        print(f"\n{report}")
    
    def display_recent_salary_changes(self, changes: List[Dict[str, Any]]):
        """Display recent salary changes"""
        if not changes:
            self.display_message("No recent salary changes.")
            return
        
        print(f"\nRECENT SALARY CHANGES:")
        print("-" * 60)
        for change in changes:
            print(f"{change['employee_name']} ({change['department']}):")
            print(f"  ${change['old_salary']:,.2f} → ${change['new_salary']:,.2f}")
            print(f"  Change: ${change['change_amount']:,.2f} ({change['change_percentage']:.1f}%)")
            print(f"  Operation: {change['operation']} - {change['timestamp']}")
            print()
    
    def display_message(self, message: str):
        """Display a general message"""
        print(f"\n{message}")
        input("Press Enter to continue...")
    
    def display_error(self, error_message: str):
        """Display an error message"""
        print(f"\nERROR: {error_message}")
        input("Press Enter to continue...")
    
    def display_success(self, success_message: str):
        """Display a success message"""
        print(f"\nSUCCESS: {success_message}")
        input("Press Enter to continue...")
    
    def confirm_action(self, message: str) -> bool:
        """Get user confirmation for an action"""
        while True:
            try:
                response = input(f"{message} (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                else:
                    print("Please enter 'y' or 'n'.")
            except KeyboardInterrupt:
                return False
            except EOFError:
                return False
    
    def get_search_criteria(self) -> Dict[str, str]:
        """Get search criteria from user"""
        criteria = {}
        
        print("\nSearch Options:")
        print("1. Search by ID")
        print("2. Search by Name")
        print("3. Search by Department")
        print("4. Search by Employee Type")
        
        while True:
            try:
                choice = input("Select search option (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    break
                else:
                    self.display_error("Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                return {}
            except EOFError:
                return {}
        
        if choice == '1':
            criteria['id'] = input("Enter Employee ID: ").strip().upper()
        elif choice == '2':
            criteria['name'] = input("Enter Name (first or last): ").strip()
        elif choice == '3':
            criteria['department'] = input("Enter Department: ").strip().upper()
        elif choice == '4':
            criteria['type'] = input("Enter Employee Type (Employee/Manager): ").strip()
        
        return criteria
    
    def display_welcome_message(self):
        """Display welcome message"""
        self.clear_screen()
        self.display_header()
        print("Welcome to the Employee Management System!")
        print("This system allows you to manage employee records")
        print("with full CRUD operations and data validation.")
        print()
        input("Press Enter to continue...")
    
    def display_goodbye_message(self):
        """Display goodbye message"""
        self.clear_screen()
        self.display_header()
        print("Thank you for using the Employee Management System!")
        print("All data has been saved successfully.")
        print()
        print("Goodbye!")
    
    def pause(self):
        """Pause for user input"""
        input("\nPress Enter to continue...")


def test_view():
    """Test function for view operations"""
    print("=== Testing View Operations ===")
    
    view = EmployeeView()
    
    # Test employee display
    from employee import Employee, Manager
    
    test_employees = [
        Employee("EMP001", "John", "Doe", "IT", "5551234567"),
        Manager("MGR001", "Jane", "Smith", "HR", "5559876543", 5, "A-101")
    ]
    
    view.display_employees(test_employees, "TEST EMPLOYEES")
    view.display_employee_details(test_employees[0])
    
    print("View tests completed.")


if __name__ == "__main__":
    test_view()
