import sqlite3
import bcrypt  # Dodaj ovu biblioteku za heširanje lozinki

class Dashboard:
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_database()

    def create_database(self):
        """Kreirajte bazu podataka i tabelu ako ne postoji."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Kreirajte tabelu ako ne postoji
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        username TEXT NOT NULL,
                        url TEXT NOT NULL,
                        password TEXT NOT NULL,
                        notes TEXT
                    )
                ''')
                conn.commit()
            print("Baza podataka uspešno kreirana.")
        except sqlite3.DatabaseError as e:
            print(f"Greška prilikom kreiranja baze: {e}")

    def add_record(self, title, username, url, password, notes):
        """Dodajte novi zapis u tabelu."""
        try:
            # Hashing lozinke pre skladištenja
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO records (title, username, url, password, notes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (title, username, url, hashed_password, notes))

                conn.commit()
            print("Zapis uspešno dodat.")
        except sqlite3.DatabaseError as e:
            print(f"Greška prilikom dodavanja zapisa: {e}")

    def get_all_records(self):
        """Vratite sve zapise iz tabele."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM records")
                records = cursor.fetchall()

            return records
        except sqlite3.DatabaseError as e:
            print(f"Greška prilikom preuzimanja zapisa: {e}")
            return []
