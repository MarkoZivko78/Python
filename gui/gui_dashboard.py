import tkinter as tk
from tkinter import Menu, Frame, Label, Entry, Button, filedialog, messagebox
from tkinter import ttk  # Dodaj ttk za Treeview
from backend.dashboard import Dashboard

class DashboardWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id  # Čuvaj user_id za buduću upotrebu
        master.title("NMD SecurePass")

        self.db = Dashboard("databases/users_database.db")  # Putanja do baze
        
        self.show_passwords = False

        # Postavi dimenzije prozora
        master.geometry("800x640")  
        
        # Kreiraj menije
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)
        
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Dodaj File meni
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Create Database", command=self.create_database_gui)
        self.file_menu.add_command(label="Import Database", command=self.import_data)
        self.file_menu.add_command(label="Export Database", command=self.export_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Dodaj Help meni
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Leva strana: Polja za unos
        self.frame_left = Frame(master, width=250, bg='lightgrey')
        self.frame_left.pack(side='left', fill='y')

        self.label_title = Label(self.frame_left, text="Title:", bg='lightgrey')
        self.label_title.pack(pady=5)
        self.entry_title = Entry(self.frame_left)
        self.entry_title.pack(pady=5)

        self.label_username = Label(self.frame_left, text="Username:", bg='lightgrey')
        self.label_username.pack(pady=5)
        self.entry_username = Entry(self.frame_left)
        self.entry_username.pack(pady=5)

        self.label_password = Label(self.frame_left, text="Password:", bg='lightgrey')
        self.label_password.pack(pady=5)
        self.entry_password = Entry(self.frame_left, show='*')
        self.entry_password.pack(pady=5)

        self.label_url = Label(self.frame_left, text="URL:", bg='lightgrey')
        self.label_url.pack(pady=5)
        self.entry_url = Entry(self.frame_left)
        self.entry_url.pack(pady=5)

        # Dodaj Label za Notes
        self.label_notes = Label(self.frame_left, text="Notes:", bg='lightgrey')
        self.label_notes.pack(pady=5)
        self.entry_notes = Entry(self.frame_left)
        self.entry_notes.pack(pady=5)

        self.button_add = Button(self.frame_left, text="Add Record", command=self.add_record)
        self.button_add.pack(pady=5)
        
        self.button_add = Button(self.frame_left, text="Delete Record")
        self.button_add.pack(pady=5)
        
        self.button_generate_password = Button(self.frame_left, text="Generate Password", command=self.generate_password)
        self.button_generate_password.pack(pady=5)

        # Desna strana: Tabela sa podacima
        self.frame_right = Frame(master)
        self.frame_right.pack(side='right', fill='both', expand=True)

        self.label_table = Label(self.frame_right, text="Tabela korisnika", font=("Arial", 16))
        self.label_table.pack(pady=10)

        # Treeview za prikaz podataka u tabeli
        self.tree = ttk.Treeview(self.frame_right, columns=("Title", "Username", "URL", "Password", "Notes"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Username", text="Username")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Password", text="Password", command=self.toggle_password)  # Poveži toggle_password
        self.tree.heading("Notes", text="Notes")
        
        self.tree.column("Title", width=100)
        self.tree.column("Username", width=100)
        self.tree.column("URL", width=150)
        self.tree.column("Password", width=100)
        self.tree.column("Notes", width=150)

        self.tree.pack(pady=10, fill='both', expand=True)

        # Učitaj korisničke podatke
        self.load_user_data()

        self.master.after(100, self.center_window)

    def center_window(self):
        """Centrira prozor na ekranu."""
        width = 800  # Širina prozora
        height = 600  # Visina prozora
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")  # Postavi geometriju prozora

    def load_user_data(self):
        """Učitaj i prikaži sve zapise iz baze."""
        records = self.db.get_all_records()
        self.original_passwords = {}  # Rečnik za čuvanje stvarnih lozinki

        # Očisti postojeće redove u Treeview-u
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ubaci podatke u Treeview
        for record in records:
            # Čuvanje stvarne lozinke
            self.original_passwords[record[0]] = record[4]  # Čuvanje stvarne lozinke sa ID kao ključ
            # Umetanje vrednosti u Treeview sa lozinkom kao "******"
            self.tree.insert("", "end", values=(record[1], record[2], record[3], "******", record[5])) 
    
    def toggle_password(self):
        """Prebacuje između prikaza i skrivanja lozinki u Treeview-u."""
        self.show_passwords = not self.show_passwords  # Promena stanja

        # Očisti postojeće redove u Treeview-u
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Učitaj i prikaži sve zapise iz baze
        records = self.db.get_all_records()  # Ponovno učitajte zapise

        # Ubaci podatke u Treeview
        for record in records:
            # Prikazivanje stvarne lozinke ili zamena sa "******"
            password_display = self.original_passwords[record[0]] if self.show_passwords else "******"
            self.tree.insert("", "end", values=(record[1], record[2], record[3], password_display, record[5]))        
                

    def add_record(self):
        """Dodajte novi zapis u bazu podataka."""
        title = self.entry_title.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        url = self.entry_url.get()
        notes = self.entry_notes.get()  # Ovo može biti opcionalno

        #print(f"Title: {title}, Username: {username}, Password: {password}, URL: {url}, Notes: {notes}")

        if title and username and password and url:  # Možete dodati notes ako je potreban
            self.db.add_record(title, username, url, password, notes)
            messagebox.showinfo("Success", "Zapis uspešno dodat!")
            self.load_user_data()  # Osveži tabelu nakon dodavanja
        else:
            messagebox.showwarning("Input Error", "Sva polja moraju biti popunjena!")  # Prilagodite ovu poruku ako je potrebno


    def create_database_gui(self):
        db_path = filedialog.asksaveasfilename(defaultextension=".db",
                                                 filetypes=[("SQLite Database", "*.db")])
        if db_path:
            self.db = Dashboard(db_path)
            messagebox.showinfo("Status", "Baza podataka uspešno kreirana.")

    def generate_password(self):
        """Generiše nasumičnu lozinku i postavlja je u polje za unos lozinke."""
        password = self.db.generate_random_password()  # Pozivamo metodu iz dashboard.py
        self.entry_password.delete(0, tk.END)  # Očisti prethodni unos
        self.entry_password.insert(0, password)  # Postavi novu lozinku

    def import_data(self):
        print("Import data functionality goes here")

    def export_data(self):
        print("Export data functionality goes here")

    def show_about(self):
        messagebox.showinfo("About", "Ovo je dashboard aplikacija.")
        
    def on_close(self):
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    dashboard_window = DashboardWindow(root, user_id=1)
    root.mainloop()
