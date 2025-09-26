Prompt 1- 
For AiDD_HW2.py, I need to be able to add multiple projects under general manager and include a revenue for each unique project. I am utilizing object oriented programming. without giving me the code, how can I add these extra fields

Response 1- 
To add multiple projects under a general manager and include a revenue for each project using object-oriented programming, you should:

1. Create a Project class with attributes like project name and revenue.
2. In your GeneralManager class, add a list (or similar collection) to store multiple Project objects.
3. Provide methods in GeneralManager to add new Project instances and access their revenues.
This way, each general manager can manage multiple projects, each with its own revenue.

I added a class named project in and added the fields projectname and revenue to it. I then attempted to set the projects = [] in the init function, but it threw an error and told me to switch it to =None instead, which I accepted. 

Prompt 2- remind me of the newer version of the get function that I can use instead of get_project_revenues(self)

Response 2- You can use a property in Python to access project revenues in a more modern way. For example, define a @property called project_revenues in your GeneralManager class. This allows you to access revenues with manager.project_revenues instead of calling a method.

I created a property instead of using the get because it is the preferred and newer way of creating a getter

Prompt 3- how can I multiply 3% times the sum of all projects? Is what I have in line 27 correct?

Response 3- You can multiply 3% (which is 0.03) by the sum of all project revenues using:

0.03 * sum(project.revenue for project in self.projects)

This expression calculates the sum of revenues for all projects and then multiplies it by 0.03

I did not need to make any changes to the code I had written. 

Prompt 4- Without giving me the code, how can i ensure a project manager is assigned to only one project at a time?

Response 4- To ensure a project manager is assigned to only one project at a time, design your ProjectManager class so it has a single project attribute (not a list). Only allow assignment or reassignment to one project at a time, and avoid methods that add multiple projects. This enforces the one-to-one relationship.

I had already created the class ProjectManager with the attribute "project" in the init function, so I did not need to make any additional changes to ensure that more than one project could not be added.

Prompt 5- how can I create a way to calculate the years served at the company so that in my property for staff, I can multiply 100 by each year served?

Response 5- You can add a method or property in your Employee class to calculate years served by subtracting the year they started from the current year.

import datetime
# ...existing code...

class Employee:
    # ...existing code...

    @property
    def years_served(self):
        current_year = datetime.datetime.now().year
        return current_year - self.year
# ...existing code... 

This was the first time I needed to import the datetime to find the current date. I thought this was a really neat feature, and the code example helped me implement the years served as a property underneath the superclass employee. I accepted this change, and from there was able to find the staff compensation. 

Prompt 6- Explain what a test module is.

Response 6- A test module is a separate Python file created to check and demonstrate that your code works as expected. It usually contains code that:

Imports your main classes or functions.
Creates objects and calls methods to verify their behavior.
Prints results or uses assertions to check correctness.

A test module is used to interactively create objects, store them in a list, and print their attributes, showing that your class hierarchy and logic function correctly. It is not part of your main application logic, but is used for testing and demonstration purposes.

I appreciated this explanation because I have never used a test module before. This explanation helped me realize that another file is required to create the objects and print information. I originally thought I needed to include the test module within the original python code, so I created a new file for the test module. 

Prompt 7- I gave the agent the following instructions for this assignment: Demonstrate that your subclass hierarchy works by writing a test module. The content of this module is at your
discretion. It DOES NOT need to be a full-fledged application. However, it should at least accomplish items 1)
and 2) below.
1. When creating new employees, the system should prompt users for
• the type of employee they would like to create.
• Based on the type of employee the user wants to create, you would ask the user for the appropriate
information.
• For this prototype, we assume that programmers can never be a manager or a staff; a staff can
never be a manager or a programmer; and that a manager can never be a programmer or a staff.
2. Once you have all the input from the user, you want to create an object of the appropriate type.
• However, you must store all the objects into the same list (to take advantage of polymorphism) in
your test of printing full compensations.

Can you give me an example of how to structure one of the class creations from the AiDD HW2 into the test module?

Response 7- From AiDD_HW2 import Project, Programmer

from AiDD_HW2 import Project, Programmer

# Example: Prompt user for Programmer details and create the object
def create_programmer():
    print("\nCreating Programmer...")
    fname = input("First name: ")
    lname = input("Last name: ")
    empid = input("Employee ID: ")
    phone = input("Phone number: ")
    year = int(input("Year started: "))
    annualsalary = float(input("Annual base salary: "))
    project_name = input("Project name: ")
    project_revenue = float(input("Project revenue: "))
    project = Project(project_name, project_revenue)
    programmer = Programmer(fname, lname, empid, phone, year, annualsalary, project)
    return programmer

# Example usage in your test module
employees = []
employees.append(create_programmer())

# Print all employees and their compensation
for emp in employees:
    print(emp)

Using this information, I was able to create new employees and an empty list to add each class of employees into the list and save it to the system. One thing I did need to add to my test module was a function for creating projects to add to each type of employee. Additionally, since general managers can have more than one project, I needed to create a loop to prompt the user to add as many projects as the general manager oversees. Lastly, I needed to create a function for the main menu system, where I could prompt users to create at least one type of each employee and add each type of employee to the employee list.  