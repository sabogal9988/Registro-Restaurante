import sqlite3
from tabulate import tabulate  # For pretty table formatting

# Connect to the database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Function to print table data
def print_table(table_name, columns):
    cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
    rows = cursor.fetchall()
    if rows:
        print(f"\n=== {table_name.upper()} ===")
        print(tabulate(rows, headers=columns, tablefmt="grid"))
    else:
        print(f"\n=== {table_name.upper()} ===\nNo data found.")

# Display users
print_table("users", ["id", "username", "role", "email"])

# Display restaurants
print_table("restaurants", ["id", "name", "address"])

# Display tables
print_table("tables", ["id", "restaurant_id", "capacity", "table_number"])

# Display reservations with joined data
cursor.execute('''
    SELECT r.id, u.username, t.table_number, r.reservation_time, r.status
    FROM reservations r
    JOIN users u ON r.user_id = u.id
    JOIN tables t ON r.table_id = t.id
''')
reservations = cursor.fetchall()
if reservations:
    print("\n=== RESERVATIONS ===")
    print(tabulate(reservations, headers=["ID", "Username", "Table", "Time", "Status"], tablefmt="grid"))
else:
    print("\n=== RESERVATIONS ===\nNo data found.")

# Close the connection
conn.close()