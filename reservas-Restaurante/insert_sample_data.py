from app.db.database import DatabaseConnection

db = DatabaseConnection()
with db.get_cursor() as cursor:
    # Insert restaurants (including new ones)
    restaurants = [
        ("La Bella Vita", "123 Olive Street, Food City"),
        ("The Golden Spoon", "456 Maple Avenue, Gourmet Town"),
        ("Ocean Breeze", "789 Coastal Road, Seaside Village"),
        ("Sunset Grill", "101 Sunset Blvd, Sunset City"),
        ("Mountain View Bistro", "202 Hilltop Lane, Mountain Town"),
        ("City Lights Diner", "303 Downtown Ave, Urban City"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO restaurants (name, address) VALUES (?, ?)", restaurants)

    # Insert tables for all restaurants
    tables = [
        # Restaurant 1: La Bella Vita (id: 1)
        (1, 4, "Table 1"),
        (1, 6, "Table 2"),
        # Restaurant 2: The Golden Spoon (id: 2)
        (2, 2, "Table 1"),
        (2, 4, "Table 2"),
        # Restaurant 3: Ocean Breeze (id: 3)
        (3, 5, "Table 1"),
        (3, 8, "Table 2"),
        # Restaurant 4: Sunset Grill (id: 4)
        (4, 4, "Table 1"),
        (4, 6, "Table 2"),
        # Restaurant 5: Mountain View Bistro (id: 5)
        (5, 2, "Table 1"),
        (5, 4, "Table 2"),
        # Restaurant 6: City Lights Diner (id: 6)
        (6, 5, "Table 1"),
        (6, 8, "Table 2"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO tables (restaurant_id, capacity, table_number) VALUES (?, ?, ?)", tables)

print("Restaurants and tables added successfully!")