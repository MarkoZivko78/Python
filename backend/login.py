import tkinter as tk
from backend.user_database import UserDatabase

class LoginHandler:
    def __init__(self):
        
        #Inicijalizuje LoginHandler i povezuje se na bazu podataka.
        self.db = UserDatabase(db_file='databases/users_database.db')

    def authenticate(self, username, password):
        #Proverava korisničko ime i lozinku, vraća user_id i username ili None.
        try:
            user = self.db.authenticate_user(username, password)
            return user  # Vraća (user_id, username) ili None
        except Exception as e:
            print(f"Greška prilikom autentifikacije: {e}")
            return None

    def close_db(self):
        #Zatvara vezu sa bazom podataka.
        self.db.close_connection()
