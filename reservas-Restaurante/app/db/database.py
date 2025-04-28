import sqlite3
from contextlib import contextmanager

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect('restaurant.db', check_same_thread=False)
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    @contextmanager
    def get_cursor(self):
        yield self.cursor
        self.connection.commit()

def init_db():
    db = DatabaseConnection()
    with db.get_cursor() as cursor:
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(100),
                role TEXT,
                email VARCHAR(100)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100),
                address VARCHAR(200)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER,
                capacity INTEGER,
                table_number VARCHAR(20),
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                table_id INTEGER,
                reservation_time DATETIME,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (table_id) REFERENCES tables(id)
            )
        ''')