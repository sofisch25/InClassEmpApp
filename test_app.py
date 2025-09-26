# Assumptions:
# - Project names and revenues are entered by the user as needed.
# - The year started is a four digit year 
# - The number of years worked cannot be negative
# - General Managers can manage multiple projects; Project Managers and Programmers are assigned to one project.
# - All employees are mutually exclusive in their roles (no overlap between types).
# - For demonstration, at least one of each employee type will be created.

from AiDD_HW2 import Employee, Project, GeneralManager, ProjectManager, Programmer, Staff

def prompt_project():
	name = input("Enter project name: ")
	revenue = float(input("Enter project revenue: "))
	return Project(name, revenue)

def create_general_manager():
	print("\nCreating General Manager")
	fname = input("First name: ")
	lname = input("Last name: ")
	empid = input("Employee ID: ")
	phone = input("Phone number: ")
	year = int(input("Year started: "))
	num_projects = int(input("How many projects does this manager oversee? "))
	projects = []
	# Prompt for each project
	for i in range(num_projects):
		print(f"Project {i+1}:")
		projects.append(prompt_project())
	return GeneralManager(fname, lname, empid, phone, year, projects)

def create_project_manager():
	print("\nCreating Project Manager")
	fname = input("First name: ")
	lname = input("Last name: ")
	empid = input("Employee ID: ")
	phone = input("Phone number: ")
	year = int(input("Year started: "))
	print("Assigning project:")
	project = prompt_project()
	return ProjectManager(fname, lname, empid, phone, year, project)

def create_programmer():
	print("\nCreating Programmer")
	fname = input("First name: ")
	lname = input("Last name: ")
	empid = input("Employee ID: ")
	phone = input("Phone number: ")
	year = int(input("Year started: "))
	annualsalary = float(input("Annual base salary: "))
	print("Assigning project:")
	project = prompt_project()
	return Programmer(fname, lname, empid, phone, year, annualsalary, project)

def create_staff():
	print("\nCreating Staff")
	fname = input("First name: ")
	lname = input("Last name: ")
	empid = input("Employee ID: ")
	phone = input("Phone number: ")
	year = int(input("Year started: "))
	annualsalary = float(input("Annual base salary: "))
	return Staff(fname, lname, empid, phone, year, annualsalary)

def main():
	employees = []
	print("Welcome to the KSD Personnel Management System Prototype!\n")
	# For demonstration, create at least one of each type
	employees.append(create_general_manager())
	employees.append(create_project_manager())
	employees.append(create_programmer())
	employees.append(create_staff())

	print("\nAll Employees and Their Compensation:")
	for emp in employees:
		print(emp)

if __name__ == "__main__":
	main()
