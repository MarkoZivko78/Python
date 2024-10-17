import csv
import sqlite3  # ili drugu biblioteku za tvoju bazu podataka
from tkinter import messagebox

class Export:

    def __init__(self, db_path):
        self.db_path = db_path

    def export_to_csv(self, csv_file_path):
        """Eksportuje sve zapise iz baze podataka u CSV fajl."""
        try:
            # Poveži se na bazu podataka
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Izvrši upit da dobiješ sve zapise iz tabele
            cursor.execute("SELECT * FROM records")  
            rows = cursor.fetchall()  # Uzmi sve redove

            # Dobij nazive kolona
            column_names = [description[0] for description in cursor.description]

            # Zapiši podatke u CSV
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)

                # Zapiši nazive kolona
                writer.writerow(column_names)

                # Zapiši sve redove
                writer.writerows(rows)

            # Obaveštenje o uspehu
            messagebox.showinfo("Success", "Baza podataka je uspešno eksportovana u CSV!")

        except Exception as e:
            # Obaveštenje o grešci
            messagebox.showerror("Error", f"Došlo je do greške: {e}")

        finally:
            cursor.close()
            conn.close()