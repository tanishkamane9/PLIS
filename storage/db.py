import sqlite3
from pathlib import Path

#Path to database file
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR /"data"
DB_PATH = DATA_DIR /"plis.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

def get_db_connection():
    """
    Create and return a SQLite database connection.
    Database file is auto-created if it does not exist 
    """
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """
    Create database tables using schema.sql
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as schema_file:
        schema_sql = schema_file.read()
        cursor.executescript(schema_sql)
        
    conn.commit()
    conn.close()
