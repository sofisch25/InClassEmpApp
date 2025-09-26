#!/usr/bin/env python3
"""
Employee Management System - Analytics Module
Handles salary analytics and reporting
"""

import logging
from typing import List, Dict, Any, Optional
from employee import Employee, Manager
from datetime import datetime

# Configure logging for analytics
analytics_logger = logging.getLogger('analytics')
analytics_logger.setLevel(logging.INFO)

class EmployeeAnalytics:
    """Analytics class for employee salary tracking and reporting"""
    
    def __init__(self):
        """Initialize analytics tracking"""
        self.salary_history = []  # Track salary changes over time
        self.analytics_logger = analytics_logger
    
    def calculate_average_salary(self, employees: List[Employee]) -> float:
        """Calculate average salary across all employees"""
        if not employees:
            return 0.0
        
        total_salary = sum(emp.salary for emp in employees)
        average = total_salary / len(employees)
        
        self.analytics_logger.info(f"Calculated average salary: ${average:,.2f} for {len(employees)} employees")
        return average
    
    def calculate_department_average_salary(self, employees: List[Employee], department: str) -> float:
        """Calculate average salary for a specific department"""
        dept_employees = [emp for emp in employees if emp.department == department.upper()]
        
        if not dept_employees:
            return 0.0
        
        total_salary = sum(emp.salary for emp in dept_employees)
        average = total_salary / len(dept_employees)
        
        self.analytics_logger.info(f"Calculated average salary for {department}: ${average:,.2f} for {len(dept_employees)} employees")
        return average
    
    def calculate_salary_statistics(self, employees: List[Employee]) -> Dict[str, Any]:
        """Calculate comprehensive salary statistics"""
        if not employees:
            return {
                'count': 0,
                'average': 0.0,
                'min': 0.0,
                'max': 0.0,
                'total': 0.0,
                'median': 0.0
            }
        
        salaries = [emp.salary for emp in employees]
        salaries.sort()
        
        stats = {
            'count': len(employees),
            'average': sum(salaries) / len(salaries),
            'min': min(salaries),
            'max': max(salaries),
            'total': sum(salaries),
            'median': salaries[len(salaries) // 2] if salaries else 0.0
        }
        
        self.analytics_logger.info(f"Calculated salary statistics: {stats}")
        return stats
    
    def track_salary_change(self, employee: Employee, old_salary: float, new_salary: float, operation: str):
        """Track salary changes for analytics"""
        change_record = {
            'timestamp': datetime.now().isoformat(),
            'employee_id': employee.id,
            'employee_name': f"{employee.fname} {employee.lname}",
            'department': employee.department,
            'old_salary': old_salary,
            'new_salary': new_salary,
            'change_amount': new_salary - old_salary,
            'change_percentage': ((new_salary - old_salary) / old_salary * 100) if old_salary > 0 else 0,
            'operation': operation
        }
        
        self.salary_history.append(change_record)
        self.analytics_logger.info(f"Tracked salary change: {change_record}")
    
    def get_salary_history(self) -> List[Dict[str, Any]]:
        """Get complete salary change history"""
        return self.salary_history.copy()
    
    def get_recent_salary_changes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent salary changes"""
        return self.salary_history[-limit:] if self.salary_history else []
    
    def calculate_salary_by_employee_type(self, employees: List[Employee]) -> Dict[str, Dict[str, Any]]:
        """Calculate salary statistics by employee type"""
        regular_employees = [emp for emp in employees if not isinstance(emp, Manager)]
        managers = [emp for emp in employees if isinstance(emp, Manager)]
        
        result = {}
        
        if regular_employees:
            result['Regular Employees'] = self.calculate_salary_statistics(regular_employees)
        
        if managers:
            result['Managers'] = self.calculate_salary_statistics(managers)
        
        return result
    
    def calculate_salary_by_department(self, employees: List[Employee]) -> Dict[str, Dict[str, Any]]:
        """Calculate salary statistics by department"""
        departments = {}
        
        for emp in employees:
            dept = emp.department
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(emp)
        
        result = {}
        for dept, dept_employees in departments.items():
            result[dept] = self.calculate_salary_statistics(dept_employees)
        
        return result
    
    def find_highest_paid_employees(self, employees: List[Employee], limit: int = 5) -> List[Employee]:
        """Find highest paid employees"""
        sorted_employees = sorted(employees, key=lambda emp: emp.salary, reverse=True)
        return sorted_employees[:limit]
    
    def find_lowest_paid_employees(self, employees: List[Employee], limit: int = 5) -> List[Employee]:
        """Find lowest paid employees"""
        sorted_employees = sorted(employees, key=lambda emp: emp.salary)
        return sorted_employees[:limit]
    
    def calculate_salary_gap_analysis(self, employees: List[Employee]) -> Dict[str, Any]:
        """Calculate salary gap analysis between managers and regular employees"""
        regular_employees = [emp for emp in employees if not isinstance(emp, Manager)]
        managers = [emp for emp in employees if isinstance(emp, Manager)]
        
        if not regular_employees or not managers:
            return {'error': 'Need both regular employees and managers for gap analysis'}
        
        regular_avg = sum(emp.salary for emp in regular_employees) / len(regular_employees)
        manager_avg = sum(emp.salary for emp in managers) / len(managers)
        
        gap_analysis = {
            'regular_employee_average': regular_avg,
            'manager_average': manager_avg,
            'absolute_gap': manager_avg - regular_avg,
            'percentage_gap': ((manager_avg - regular_avg) / regular_avg * 100) if regular_avg > 0 else 0,
            'regular_count': len(regular_employees),
            'manager_count': len(managers)
        }
        
        self.analytics_logger.info(f"Calculated salary gap analysis: {gap_analysis}")
        return gap_analysis
    
    def generate_salary_report(self, employees: List[Employee]) -> str:
        """Generate a comprehensive salary report"""
        report = []
        report.append("=" * 60)
        report.append("EMPLOYEE SALARY ANALYTICS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall statistics
        overall_stats = self.calculate_salary_statistics(employees)
        report.append("OVERALL SALARY STATISTICS:")
        report.append(f"  Total Employees: {overall_stats['count']}")
        report.append(f"  Average Salary: ${overall_stats['average']:,.2f}")
        report.append(f"  Minimum Salary: ${overall_stats['min']:,.2f}")
        report.append(f"  Maximum Salary: ${overall_stats['max']:,.2f}")
        report.append(f"  Median Salary: ${overall_stats['median']:,.2f}")
        report.append(f"  Total Payroll: ${overall_stats['total']:,.2f}")
        report.append("")
        
        # Department breakdown
        dept_stats = self.calculate_salary_by_department(employees)
        report.append("SALARY BY DEPARTMENT:")
        for dept, stats in dept_stats.items():
            report.append(f"  {dept}:")
            report.append(f"    Count: {stats['count']}")
            report.append(f"    Average: ${stats['average']:,.2f}")
            report.append(f"    Range: ${stats['min']:,.2f} - ${stats['max']:,.2f}")
        report.append("")
        
        # Employee type breakdown
        type_stats = self.calculate_salary_by_employee_type(employees)
        report.append("SALARY BY EMPLOYEE TYPE:")
        for emp_type, stats in type_stats.items():
            report.append(f"  {emp_type}:")
            report.append(f"    Count: {stats['count']}")
            report.append(f"    Average: ${stats['average']:,.2f}")
            report.append(f"    Range: ${stats['min']:,.2f} - ${stats['max']:,.2f}")
        report.append("")
        
        # Gap analysis
        gap_analysis = self.calculate_salary_gap_analysis(employees)
        if 'error' not in gap_analysis:
            report.append("SALARY GAP ANALYSIS:")
            report.append(f"  Regular Employee Average: ${gap_analysis['regular_employee_average']:,.2f}")
            report.append(f"  Manager Average: ${gap_analysis['manager_average']:,.2f}")
            report.append(f"  Absolute Gap: ${gap_analysis['absolute_gap']:,.2f}")
            report.append(f"  Percentage Gap: {gap_analysis['percentage_gap']:.1f}%")
            report.append("")
        
        # Top earners
        top_earners = self.find_highest_paid_employees(employees, 5)
        report.append("TOP 5 EARNERS:")
        for i, emp in enumerate(top_earners, 1):
            report.append(f"  {i}. {emp.fname} {emp.lname} ({emp.department}) - ${emp.salary:,.2f}")
        report.append("")
        
        # Recent changes
        recent_changes = self.get_recent_salary_changes(5)
        if recent_changes:
            report.append("RECENT SALARY CHANGES:")
            for change in recent_changes:
                report.append(f"  {change['employee_name']}: ${change['old_salary']:,.2f} → ${change['new_salary']:,.2f} ({change['operation']})")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def test_analytics():
    """Test function for analytics operations"""
    print("=== Testing Analytics Operations ===")
    
    from employee import Employee, Manager
    
    # Create test employees
    employees = [
        Employee("EMP001", "Alice", "Smith", "HR", "5551234567", 55000.0),
        Employee("EMP002", "Bob", "Johnson", "IT", "5552345678", 65000.0),
        Manager("MGR001", "Carol", "Lee", "IT", "5553456789", 85000.0, 5, "A-101"),
        Employee("EMP003", "David", "Kim", "FIN", "5554567890", 60000.0),
        Manager("MGR002", "Eva", "Brown", "HR", "5555678901", 75000.0, 3, "B-202")
    ]
    
    analytics = EmployeeAnalytics()
    
    # Test average salary calculation
    avg_salary = analytics.calculate_average_salary(employees)
    print(f"Average salary: ${avg_salary:,.2f}")
    
    # Test department average
    it_avg = analytics.calculate_department_average_salary(employees, "IT")
    print(f"IT department average: ${it_avg:,.2f}")
    
    # Test salary statistics
    stats = analytics.calculate_salary_statistics(employees)
    print(f"Salary statistics: {stats}")
    
    # Test salary gap analysis
    gap_analysis = analytics.calculate_salary_gap_analysis(employees)
    print(f"Salary gap analysis: {gap_analysis}")
    
    # Test salary report generation
    report = analytics.generate_salary_report(employees)
    print("\n" + report)
    
    print("Analytics tests completed.")


if __name__ == "__main__":
    test_analytics()
