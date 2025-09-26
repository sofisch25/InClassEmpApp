import datetime

class Employee:
    def __init__ (self, fname, lname, empid, phone, year ):
        self.fname = fname
        self.lname = lname
        self.empid = empid
        self.phone = phone
        self.year = year

    @property
    def years_of_service(self):
        current_year = datetime.datetime.now().year
        return max(0, current_year - self.year)

class Project:

    def __init__ (self, projectname, revenue):
        self.projectname = projectname
        self.revenue = float(revenue)

class GeneralManager(Employee):
    def __init__ (self, fname, lname, empid, phone, year, projects):
        super().__init__(fname, lname, empid, phone, year)
        self.projects = projects

    def calculateCompensation(self):
        return 0.03 * sum(project.revenue for project in self.projects)

    def __str__ (self):
        projects_str = ', '.join([project.projectname for project in self.projects])
        return (f"General Manager: {self.fname} {self.lname}, ID: {self.empid}, Phone: {self.phone}, "
                f"Year Started: {self.year}, Projects: [{projects_str}], "
                f"Total Compensation: ${self.calculateCompensation():.2f}")


class ProjectManager(Employee):
    def __init__ (self, fname, lname, empid,phone, year, project):
        super().__init__(fname, lname, empid, phone, year)
        self.project = project

    def calculateCompensation(self):
        return 0.05 * (self.project.revenue if self.project else 0)

    def __str__ (self):
        project_str = self.project.projectname if self.project else 'None'
        return (f"Project Manager: {self.fname} {self.lname}, ID: {self.empid}, Phone: {self.phone}, "
                f"Year Started: {self.year}, Project: {project_str}, "
                f"Total Compensation: ${self.calculateCompensation():.2f}")

class Programmer(Employee):
    def __init__ (self, fname, lname, empid, phone, year, annualsalary, project):
        super().__init__(fname, lname, empid, phone, year)
        self.annualsalary = float(annualsalary)
        self.project = project

    def calculateCompensation(self):
        return self.annualsalary + 0.01 * (self.project.revenue if self.project else 0)

    def __str__ (self):
        project_str = self.project.projectname if self.project else 'None'
        return (f"Programmer: {self.fname} {self.lname}, ID: {self.empid}, Phone: {self.phone}, "
                f"Year Started: {self.year}, Annual Salary: ${self.annualsalary:.2f}, Project: {project_str}, "
                f"Total Compensation: ${self.calculateCompensation():.2f}")

class Staff(Employee):
    def __init__ (self, fname, lname, empid, phone, year, annualsalary):
        super().__init__(fname, lname, empid, phone, year)
        self.annualsalary = float(annualsalary)

    def calculateCompensation(self):
        return self.annualsalary + 100 * self.years_of_service

    def __str__ (self):
        return (f"Staff: {self.fname} {self.lname}, ID: {self.empid}, Phone: {self.phone}, "
                f"Year Started: {self.year}, Annual Salary: ${self.annualsalary:.2f}, "
                f"Years Served: {self.years_of_service}, Total Compensation: ${self.calculateCompensation():.2f}")
