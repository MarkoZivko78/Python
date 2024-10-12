import tkinter as tk
from tkinter import Menu, Frame, Label, Text, filedialog, messagebox
from backend.dashboard import Dashboard

class DashboardWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id  # Čuvaj user_id za buduću upotrebu
        master.title("NMD SecurePass")

        # Postavi dimenzije prozora
        master.geometry("800x640")  
        
        # Kreiraj menije
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)
        
        # Povezivanje zatvaranja prozora sa on_close metodom
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

        # Raspored: Leva strana za dodelu grupa, desna strana za tabelu
        self.frame_left = Frame(master, width=250, bg='lightgrey')
        self.frame_left.pack(side='left', fill='y')

        self.frame_right = Frame(master)
        self.frame_right.pack(side='right', fill='both', expand=True)

        # Leva strana: Prikaz za dodelu grupa
        self.label_groups = Label(self.frame_left, text="Dodeli grupe", bg='lightgrey')
        self.label_groups.pack(pady=10)

        self.text_groups = Text(self.frame_left, height=20, width=30)
        self.text_groups.pack(pady=10)

        # Desna strana: Prikaz tabele
        self.label_table = Label(self.frame_right, text="Tabela korisnika", font=("Arial", 16))
        self.label_table.pack(pady=10)

        self.text_table = Text(self.frame_right, height=20, width=50)
        self.text_table.pack(pady=10)

        # Učitaj podatke vezane za user_id (ovo je samo primer)
        self.load_user_data()

        # Centriraj prozor nakon što su svi elementi dodani
        self.master.after(100, self.center_window)  # Odelay sa 100ms pre centriranja

    def center_window(self):
        """Centrira prozor na ekranu."""
        width = 800  # Širina prozora
        height = 600  # Visina prozora
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")  # Postavi geometriju prozora

    def load_user_data(self):
        # Ovdje možeš učitati i prikazati podatke vezane za user_id
        # Na primer, učitavanje podataka iz baze i popunjavanje text_table
        self.text_table.insert(tk.END, f"Prikazujem podatke za korisnika ID: {self.user_id}")

    def create_database_gui(self):
        # Otvorite dijalog za odabir lokacije gde će se sačuvati nova baza podataka
        db_path = filedialog.asksaveasfilename(defaultextension=".db",
                                                 filetypes=[("SQLite Database", "*.db")])
        if db_path:
            dashboard = Dashboard(db_path)  # Kreirajte instancu Dashboard
            messagebox.showinfo("Status", "Baza podataka uspešno kreirana.")

    def import_data(self):
        print("Import data functionality goes here")

    def export_data(self):
        print("Export data functionality goes here")

    def show_about(self):
        messagebox.showinfo("About", "Ovo je dashboard aplikacija.")
        
    def on_close(self):
        """Zatvaranje GUI-a."""
        self.master.quit()  # Završava mainloop
        self.master.destroy()  # Zatvara prozor     

if __name__ == "__main__":
    root = tk.Tk()
    dashboard_window = DashboardWindow(root, user_id=1)  # Primer sa user_id
    root.mainloop()  # Pokreni glavnu petlju
