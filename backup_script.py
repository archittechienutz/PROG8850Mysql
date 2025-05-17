# Automates backing up a single MySQL database (school_db) to a timestamped SQL file.
# Uses TCP connection to ensure compatibility with Docker-based MySQL.

#!/usr/bin/env python3
import subprocess
import datetime
import os

# --- Configuration ---
DB_USER    = "root"             # MySQL username
db_pass    = "Secret5555"      # Password for the MySQL user
DB_HOST    = "127.0.0.1"        # Connect via TCP to the MySQL server
DB_NAME    = "school_db"        # Name of the database to back up
BACKUP_DIR = "./backups"       # Directory to store backup files
# ---------------------

def ensure_backup_dir():
    """
    Create the backup directory if it doesn't exist.
    """
    os.makedirs(BACKUP_DIR, exist_ok=True)


def make_backup():
    """
    Runs mysqldump to export the DB into a timestamped .sql file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{BACKUP_DIR}/backup_{timestamp}.sql"

    cmd = [
        "mysqldump",          # Backup utility
        "-u", DB_USER,        # Username flag
        f"-p{db_pass}",       # Password flag (no space)
        "--host", DB_HOST,    # Host flag (enforce TCP)
        DB_NAME               # Target database name
    ]

    # Execute the dump and write directly to file
    with open(filename, "w") as out:
        subprocess.run(cmd, stdout=out, check=True)

    print(f"Backup created: {filename}")


if __name__ == "__main__":
    ensure_backup_dir()
    make_backup()