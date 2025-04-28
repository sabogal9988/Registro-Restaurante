from abc import ABC, abstractmethod
from app.db.database import DatabaseConnection
import bcrypt

class User(ABC):
    @abstractmethod
    def get_role(self):
        pass

class Client(User):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_role(self):
        return 'client'

class Admin(User):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_role(self):
        return 'admin'

class UserFactory:
    @staticmethod
    def create_user(user_type, username, email, password):
        db = DatabaseConnection()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        with db.get_cursor() as cursor:
            cursor.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)',
                         (username, hashed, user_type, email))
        
        if user_type == 'client':
            return Client(username, email)
        elif user_type == 'admin':
            return Admin(username, email)