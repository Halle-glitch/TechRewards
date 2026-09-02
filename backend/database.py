import sqlite3

# Connect to the database
connection = sqlite3.connect("techrewards.db")

# Create the technicians table
def create_tables():
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS technicians (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            employee_number TEXT NOT NULL)""")

    connection.commit()

# Create the tables
create_tables()