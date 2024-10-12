import sqlite3
from sqlite3 import Error
import bcrypt  # Koristi bcrypt za heširanje lozinki
from tkinter import messagebox

class UserDatabase:
    def __init__(self, db_file='databases/users_database.db'):
        #Inicijalizacija klase i povezivanje na bazu podataka.
        self.db_file = db_file
        self.create_connection()
        self.create_table()

    def create_connection(self):
        #Kreira vezu sa SQLite bazom podataka.
        try:
            self.connection = sqlite3.connect(self.db_file)
            return "Uspešna konekcija na SQLite bazu podataka."
        except Error as e:
            return f"Greška prilikom povezivanja na bazu podataka: {e}"

    def close_connection(self):
        #Zatvara vezu sa bazom podataka.
        if self.connection:
            self.connection.close()
            return "Veza sa bazom podataka je zatvorena."

    def create_table(self):
        #Kreira tabelu za korisnike ako ne postoji.
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def add_user(self, username, email, password):
        #Dodaje novog korisnika u bazu podataka sa heširanom lozinkom.
        try:
            # Heširanje lozinke pre čuvanja
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            insert_query = '''
            INSERT INTO users (username, email, password) 
            VALUES (?, ?, ?)'''
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (username, email, hashed_password))
            self.connection.commit()
            cursor.close()
            return f"Korisnik '{username}' uspešno dodat."
        except sqlite3.IntegrityError:
            return f"Greška: Korisnik sa emailom '{email}' već postoji."


    def get_all_users(self):
        #Vraća sve korisnike iz baze podataka.
        select_query = 'SELECT * FROM users'
        cursor = self.connection.cursor()
        cursor.execute(select_query)
        users = cursor.fetchall()
        cursor.close()
        return users

    def get_user_by_id(self, user_id):
        #Vraća korisnika po ID-u.
        select_query = 'SELECT * FROM users WHERE user_id = ?'
        cursor = self.connection.cursor()
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def get_user_by_email(self, email):
        #Vraća korisnika po emailu.
        select_query = 'SELECT * FROM users WHERE email = ?'
        cursor = self.connection.cursor()
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def update_user(self, user_id, username, email, password):
        #Ažurira korisnika na osnovu user_id.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        update_query = 'UPDATE users SET username = ?, email = ?, password = ? WHERE user_id = ?'
        cursor = self.connection.cursor()
        cursor.execute(update_query, (username, email, hashed_password, user_id))
        self.connection.commit()
        cursor.close()
        return f"Korisnik sa ID-jem {user_id} je uspešno ažuriran."

    def delete_user(self, user_id):
        #Briše korisnika iz baze podataka po user_id.
        delete_query = 'DELETE FROM users WHERE user_id = ?'
        cursor = self.connection.cursor()
        cursor.execute(delete_query, (user_id,))
        self.connection.commit()
        cursor.close()
        return f"Korisnik sa ID-jem {user_id} je uspešno obrisan."

    def authenticate_user(self, username, password):
        #Proverava da li korisnik postoji i vraća njegov user_id i username.
        select_query = 'SELECT user_id, username, password FROM users WHERE username = ?'
        cursor = self.connection.cursor()
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return user[0], user[1]  # Vraća user_id i username
        return None


##########################################################################################################################################################################################
#DELETE FROM users;  -- Isprazni tabelu
#DELETE FROM sqlite_sequence WHERE name='users';  -- Resetuj ID
##########################################################################################################################################################################################