import sqlite3
import string
import random
import os

class Dashboard:
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_database()

    def create_database(self):
        """Kreirajte bazu podataka i tabelu ako ne postoji.""" 
        # Proverite da li baza podataka već postoji
        if not os.path.exists(self.db_path):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    # Kreirajte tabelu ako ne postoji
                    cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        username TEXT NOT NULL,
                        url TEXT NOT NULL,
                        password TEXT NOT NULL,
                        notes TEXT
                    )''')
                    conn.commit()
                #print("Baza podataka uspešno kreirana.")
            except sqlite3.DatabaseError as e:
                print(f"Greška prilikom kreiranja baze: {e}")
        else:
            print("Baza podataka već postoji, tabela se neće ponovo kreirati.")

    def add_record(self, title, username, url, password, notes):
        """Dodajte novi zapis u tabelu."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO records (title, username, url, password, notes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (title, username, url, password, notes))  # Čuvanje originalne lozinke
                
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

                readable_records = []
                for record in records:
                    id, title, username, url, password, notes = record
                    # Dodajte zapis sa originalnim lozinkama
                    readable_records.append((id, title, username, url, password, notes))

            return readable_records
        except sqlite3.DatabaseError as e:
            print(f"Greška prilikom preuzimanja zapisa: {e}")
            return []
        
    def delete_record(self, record_id):
        """Brisanje zapisa na osnovu ID-a iz tabele records."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Brisanje zapisa iz tabele
                cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
                conn.commit()

                if cursor.rowcount > 0:
                    print(f"Record sa ID-om {record_id} je uspešno obrisan.")
                else:
                    print(f"Nije pronađen zapis sa ID-om {record_id}.")

        except sqlite3.DatabaseError as e:
            print(f"Greška prilikom brisanja zapisa: {e}")    
        
    def generate_random_password(self, length=12):
        """Generiše nasumičnu lozinku određene dužine."""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
