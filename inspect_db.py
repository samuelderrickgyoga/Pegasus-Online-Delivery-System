import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/progs.db')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    # Get row count for each table
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  Rows: {count}")

conn.close()
