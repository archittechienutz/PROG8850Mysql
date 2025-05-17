# Reads SQL commands from changes.sql and applies them to the school_db database.
# Uses mysql-connector to connect over TCP and execute each statement sequentially.

#!/usr/bin/env python3
import mysql.connector
import sys

# --- Configuration ---
DB_CONFIG = {
    "user":     "root",        # MySQL user with privileges
    "password": "Secret5555",  # Password for the MySQL user
    "host":     "127.0.0.1",    # Connect via TCP
    "database": "school_db"    # Target database
}
SQL_FILE = "changes.sql"        # File containing SQL statements
# ---------------------

def load_sql(filename):
    """
    Load the entire SQL file contents into a string.
    """
    with open(filename, "r") as f:
        return f.read()


def apply_changes(sql_text):
    """
    Split the SQL text on semicolons and execute each non-empty statement.
    """
    # Connect to MySQL
    cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = cnx.cursor()

    # Execute each statement
    for stmt in sql_text.split(";"):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt + ";")
            print(f"Executed: {stmt[:50]}...")

    # Commit and close
    cnx.commit()
    cursor.close()
    cnx.close()
    print("All changes deployed.")


if __name__ == "__main__":
    try:
        sql_commands = load_sql(SQL_FILE)
        apply_changes(sql_commands)
    except Exception as e:
        print(f"Error during deployment: {e}", file=sys.stderr)
        sys.exit(1)