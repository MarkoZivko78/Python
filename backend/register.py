import re
from backend.user_database import UserDatabase

def register_user(username, email, password, confirm_password):
    # Inicijalizacija baze podataka
    db = UserDatabase(db_file='databases/users_database.db')  # Prosledi putanju do baze

    # Provera da li lozinke odgovaraju
    if password != confirm_password:
        return False, "Greška: Lozinke se ne poklapaju."

    # Provera validnosti email-a (možeš koristiti regularne izraze za validaciju)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Greška: Nevalidna email adresa."

    # Provera minimalne dužine lozinke (npr. najmanje 6 karaktera)
    if len(password) < 6:
        return False, "Greška: Lozinka mora sadržati najmanje 6 karaktera."

    # Provera da li korisnik već postoji u bazi
    existing_user = db.get_user_by_email(email)  # Ova metoda treba biti dodata u UserDatabase
    if existing_user:
        return False, f"Greška: Korisnik sa emailom '{email}' već postoji."

    # Dodavanje novog korisnika u bazu
    try:
        db.add_user(username, email, password)
        return True, f"Uspešna registracija korisnika '{username}'!"
    except Exception as e:
        return False, f"Greška prilikom registracije korisnika: {e}"
    finally:
        db.close_connection()
