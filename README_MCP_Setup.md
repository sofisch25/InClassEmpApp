# MCP SQLite Server Setup

This directory contains a simple MCP (Model Context Protocol) server for interacting with your `employees.db` SQLite database.

## Files Created

- `mcp_sqlite_server.py` - The main MCP server implementation
- `mcp_server_config.json` - Configuration file for Cursor to use the MCP server
- `requirements.txt` - Dependencies (none required - uses Python standard library)
- `README_MCP_Setup.md` - This setup guide

## Database Schema

Your `employees.db` database contains:
- `departments` table with `id` and `name` columns
- `employees` table with `id`, `name`, `department_id`, `salary`, and `hire_date` columns

## Setup Instructions

### 1. Configure Cursor to Use the MCP Server

Add the following configuration to your Cursor settings:

1. Open Cursor Settings (Ctrl+,)
2. Search for "MCP" or "Model Context Protocol"
3. Add the MCP server configuration from `mcp_server_config.json`

Or manually add this to your Cursor settings JSON:

```json
{
  "mcpServers": {
    "sqlite-employees": {
      "command": "python",
      "args": ["mcp_sqlite_server.py"],
      "env": {
        "DATABASE_PATH": "employees.db"
      }
    }
  }
}
```

### 2. Restart Cursor

After adding the MCP server configuration, restart Cursor to load the new server.

### 3. Test the Setup

Once Cursor restarts, you should be able to use the following tools:

- **query_database**: Execute SELECT queries
- **write_database**: Execute INSERT, UPDATE, DELETE queries  
- **get_schema**: Get database schema information

## Available Tools

### query_database
Execute SELECT queries on the database.

**Parameters:**
- `query` (string): SQL SELECT query to execute
- `params` (array, optional): Query parameters

**Example:**
```json
{
  "name": "query_database",
  "arguments": {
    "query": "SELECT * FROM employees WHERE department_id = ?",
    "params": ["1"]
  }
}
```

### write_database
Execute INSERT, UPDATE, or DELETE queries.

**Parameters:**
- `query` (string): SQL query to execute
- `params` (array, optional): Query parameters

**Example:**
```json
{
  "name": "write_database",
  "arguments": {
    "query": "INSERT INTO employees (name, department_id, salary, hire_date) VALUES (?, ?, ?, ?)",
    "params": ["John Doe", "1", "50000", "2024-01-01"]
  }
}
```

### get_schema
Get database schema information.

**Parameters:** None

## Usage Examples

Once set up, you can ask Cursor AI to:

- "Show me all employees in the database"
- "Add a new employee named Jane Smith to department 1"
- "What's the database schema?"
- "Find employees with salary greater than 60000"
- "Update employee ID 1's salary to 55000"

## Troubleshooting

1. **Server not starting**: Make sure Python is in your PATH and the database file exists
2. **Permission errors**: Ensure the database file is readable/writable
3. **Connection issues**: Check that `employees.db` is in the same directory as the MCP server

## Security Note

This is a simple MCP server for local development. The database file should be kept secure and not exposed to external networks.
