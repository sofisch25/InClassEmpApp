#!/usr/bin/env python3
"""
Simple MCP Server for SQLite Database Operations
This server provides tools to interact with the employees.db database
"""

import json
import sqlite3
import os
import sys
from typing import Any, Dict, List, Optional

class SQLiteMCPServer:
    def __init__(self, database_path: str = "employees.db"):
        self.database_path = database_path
        self.connection = None
        
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}", file=sys.stderr)
            return False
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        """Execute a SELECT query and return results"""
        if not self.connection:
            return {"error": "Not connected to database"}
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(row))
            
            return {
                "success": True,
                "data": results,
                "row_count": len(results)
            }
        except sqlite3.Error as e:
            return {"error": f"Database error: {e}"}
    
    def execute_write(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        """Execute INSERT, UPDATE, or DELETE queries"""
        if not self.connection:
            return {"error": "Not connected to database"}
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            
            return {
                "success": True,
                "rows_affected": cursor.rowcount,
                "last_row_id": cursor.lastrowid
            }
        except sqlite3.Error as e:
            self.connection.rollback()
            return {"error": f"Database error: {e}"}
    
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema information"""
        if not self.connection:
            return {"error": "Not connected to database"}
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            schema = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                schema[table_name] = [dict(col) for col in columns]
            
            return {"success": True, "schema": schema}
        except sqlite3.Error as e:
            return {"error": f"Database error: {e}"}

def main():
    """Main function to run the MCP server"""
    # Get database path from environment or use default
    database_path = os.getenv("DATABASE_PATH", "employees.db")
    
    # Initialize server
    server = SQLiteMCPServer(database_path)
    
    if not server.connect():
        print("Failed to connect to database", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Read MCP messages from stdin
        for line in sys.stdin:
            if not line.strip():
                continue
                
            try:
                message = json.loads(line.strip())
                handle_message(server, message)
            except json.JSONDecodeError as e:
                send_error(f"Invalid JSON: {e}")
            except Exception as e:
                send_error(f"Unexpected error: {e}")
    
    except KeyboardInterrupt:
        pass
    finally:
        server.disconnect()

def handle_message(server: SQLiteMCPServer, message: Dict[str, Any]):
    """Handle incoming MCP messages"""
    method = message.get("method")
    params = message.get("params", {})
    request_id = message.get("id")
    
    if method == "tools/list":
        send_response(request_id, {
            "tools": [
                {
                    "name": "query_database",
                    "description": "Execute a SELECT query on the database",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL SELECT query to execute"
                            },
                            "params": {
                                "type": "array",
                                "description": "Query parameters",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "write_database",
                    "description": "Execute INSERT, UPDATE, or DELETE queries",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL query to execute"
                            },
                            "params": {
                                "type": "array",
                                "description": "Query parameters",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_schema",
                    "description": "Get database schema information",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        })
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "query_database":
            query = arguments.get("query")
            query_params = tuple(arguments.get("params", []))
            result = server.execute_query(query, query_params)
            send_response(request_id, result)
        
        elif tool_name == "write_database":
            query = arguments.get("query")
            query_params = tuple(arguments.get("params", []))
            result = server.execute_write(query, query_params)
            send_response(request_id, result)
        
        elif tool_name == "get_schema":
            result = server.get_schema()
            send_response(request_id, result)
        
        else:
            send_error(f"Unknown tool: {tool_name}", request_id)
    
    else:
        send_error(f"Unknown method: {method}", request_id)

def send_response(request_id: Optional[str], result: Dict[str, Any]):
    """Send a response message"""
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }
    print(json.dumps(response))
    sys.stdout.flush()

def send_error(message: str, request_id: Optional[str] = None):
    """Send an error message"""
    error = {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -1,
            "message": message
        }
    }
    print(json.dumps(error))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
