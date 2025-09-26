# Employee Management System (MVC + AI Reflection)

A comprehensive console-based Employee Management System built using MVC architecture with full CRUD operations, logging, and SQL display capabilities.

## Team Members
[Your Name Here] - Assignment 3: HR Employee Management System

## Features

### Core Functionality
- **Create Employees**: Add new regular employees or managers
- **Edit Employees**: Update existing employee information
- **Delete Employees**: Remove employees from the system
- **Display Employees**: View all employees with detailed information
- **Search Employees**: Find employees by ID, name, department, or type
- **Department Summary**: View statistics by department
- **Data Backup**: Create backup copies of employee data
- **SQL Operations Log**: View all database operations performed

### Technical Features
- **MVC Architecture**: Clean separation of Model, View, and Controller
- **Object-Oriented Design**: Inheritance and polymorphism with Employee/Manager classes
- **Data Validation**: Comprehensive input validation and sanitization
- **Logging**: Complete operation logging with timestamps
- **SQL Display**: Real-time SQL operation tracking and display
- **Error Handling**: Graceful error handling with user-friendly messages

## File Structure

```
├── employee.py              # Model layer - Employee and Manager classes
├── EmployeeData.py          # Data layer - CSV operations
├── EmployeeView.py          # View layer - Console UI
├── EmployeeApp.py           # Controller layer - Main application
├── employee_data.csv        # Data storage file
├── .prompt/dev_notes.md     # AI development reflection
├── README.md               # This file
└── requirements.txt        # Dependencies (none required)
```

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- No additional dependencies required (uses standard library only)

### Setup Instructions
1. Clone or download the project files
2. Ensure all Python files are in the same directory
3. Run the application: `python EmployeeApp.py`

## Usage

### Starting the Application
```bash
python EmployeeApp.py
```

### Main Menu Options
1. **Create New Employee** - Add a new employee or manager
2. **Edit Existing Employee** - Update employee information
3. **Delete Existing Employee** - Remove an employee
4. **Display All Employees** - View all employees
5. **Search Employees** - Find employees by criteria
6. **Display Department Summary** - View department statistics
7. **Backup Data** - Create a backup of employee data
8. **View SQL Operations Log** - See all database operations
9. **Quit** - Exit the application

### Employee Types

#### Regular Employee
- Employee ID (read-only after creation)
- First Name (no digits allowed)
- Last Name (no digits allowed)
- Department (exactly 3 uppercase letters)
- Phone Number (10 digits, any format accepted)

#### Manager (inherits from Employee)
- All Employee attributes plus:
- Team Size (non-negative integer)
- Office Number (optional string)

### Data Validation

#### Name Validation
- Cannot be empty
- Cannot contain digits
- Automatically formatted (title case)

#### Department Validation
- Must be exactly 3 uppercase letters
- Examples: HR, IT, FIN, SAL, OPS

#### Phone Number Validation
- Must be exactly 10 digits
- Accepts various formats: (555)-123-4567, 555.123.4567, 5551234567
- Automatically sanitized to 10-digit format

## Sample Data

The application comes with sample data including:
- 5 Regular Employees
- 3 Managers
- 3 Departments (HR, IT, FIN)

## Logging

### Application Logs
- `employee_app.log` - Main application operations
- `employee_test.log` - Employee creation and validation tests

### SQL Operations Log
- Real-time tracking of all database operations
- Timestamps and operation details
- Accessible through menu option 8

## Testing

### Run Employee Model Tests
```bash
python employee.py
```

### Run Data Layer Tests
```bash
python EmployeeData.py
```

### Run View Layer Tests
```bash
python EmployeeView.py
```

## AI Development Reflection

This project was developed with significant AI assistance. See `.prompt/dev_notes.md` for detailed analysis of:
- AI performance and capabilities
- Time savings analysis
- OOP challenges and solutions
- Business perspective on AI-assisted development
- ROI estimation and recommendations

## Error Handling

The application includes comprehensive error handling:
- Input validation with clear error messages
- File operation error handling
- Database connection error handling
- Graceful handling of user interruptions (Ctrl+C)

## Security Considerations

- Input sanitization for all user inputs
- Phone number format validation
- Department code validation
- File operation safety checks

## Future Enhancements

Potential improvements for future versions:
- Database integration (SQLite/PostgreSQL)
- Web-based interface
- Advanced reporting features
- Employee photo support
- Department hierarchy management
- Performance metrics and analytics

## Troubleshooting

### Common Issues

1. **File Not Found Error**
   - Ensure all files are in the same directory
   - Check file permissions

2. **Validation Errors**
   - Follow input format requirements
   - Check phone number format
   - Ensure department codes are 3 uppercase letters

3. **CSV File Issues**
   - The application will create the CSV file if it doesn't exist
   - Check file permissions for read/write access

### Getting Help

If you encounter issues:
1. Check the log files for error details
2. Verify all files are present and properly named
3. Ensure Python 3.7+ is installed
4. Check file permissions in the application directory

## License

This project is created for educational purposes as part of Assignment 3.

## Contact

For questions or issues, please refer to the development team or course instructor.
