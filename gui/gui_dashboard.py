import tkinter as tk
from tkinter import Menu, Frame, Label, Entry, Button, filedialog, messagebox, Text
from tkinter import ttk  # Dodaj ttk za Treeview
from backend.record_dash_database import Dashboard
from backend.export_records import Export
import pyperclip
import sqlite3

class DashboardWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id  # Čuvaj user_id za buduću upotrebu
        master.title("NMD SecurePass")

         # Putanja do baze podataka
        db_path = "databases/users_database.db"
        self.db = Dashboard(db_path)  # Kreiraj instancu Dashboard klase
        self.show_passwords = False
        master.geometry("1000x750")  
        
        # Kreiraj menije
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)        
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Dodaj File meni
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Create Database", command=self.create_database_gui, state=tk.DISABLED)
        self.file_menu.add_command(label="Import Database", command=self.import_data, state=tk.DISABLED)
        self.file_menu.add_command(label="Export Records", command=self.export_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Dodaj Help meni
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Leva strana: Polja za unos
        self.frame_left = tk.Frame(master, width=250, bg='lightgrey', padx=10, pady=10)
        self.frame_left.pack(side='left', fill='y')

        # Title Entry
        self.label_title = tk.Label(self.frame_left, text="Title:", bg='lightgrey', height=1)
        self.label_title.pack(pady=(5, 2))
        self.entry_title = tk.Entry(self.frame_left, width=30, bg='lightgrey')
        self.entry_title.pack(pady=(0, 10))
        self.entry_title.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_title.bind("<FocusOut>", self.on_entry_focus_out)

        # Username Entry
        self.label_username = tk.Label(self.frame_left, text="Username:", bg='lightgrey', height=1)
        self.label_username.pack(pady=(5, 2))
        self.entry_username = tk.Entry(self.frame_left, width=30, bg='lightgrey')
        self.entry_username.pack(pady=(0, 10))
        self.entry_username.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_username.bind("<FocusOut>", self.on_entry_focus_out)

        # Password Entry
        self.label_password = tk.Label(self.frame_left, text="Password:", bg='lightgrey', height=1)
        self.label_password.pack(pady=(5, 2))
        self.entry_password = tk.Entry(self.frame_left, show='*', width=30, bg='lightgrey')
        self.entry_password.pack(pady=(0, 10))
        self.entry_password.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_password.bind("<FocusOut>", self.on_entry_focus_out)
        
        # Generate Password Button
        self.button_generate_password = Button(self.frame_left, text="Generate Password", command=self.generate_password)
        self.button_generate_password.pack(pady=(5, 10))

        # URL Entry
        self.label_url = tk.Label(self.frame_left, text="URL:", bg='lightgrey', height=1)
        self.label_url.pack(pady=(5, 2))
        self.entry_url = tk.Entry(self.frame_left, width=30, bg='lightgrey')
        self.entry_url.pack(pady=(0, 10))
        self.entry_url.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_url.bind("<FocusOut>", self.on_entry_focus_out)

        # Notes Text
        self.label_notes = tk.Label(self.frame_left, text="Notes:", bg='lightgrey', height=1)
        self.label_notes.pack(pady=5)
        self.entry_notes = tk.Text(self.frame_left, width=30, height=5, bg='lightgrey')
        self.entry_notes.pack(pady=5)
        self.entry_notes.bind("<FocusIn>", self.on_text_focus_in)
        self.entry_notes.bind("<FocusOut>", self.on_text_focus_out)

        # Add Record Button
        self.button_add = Button(self.frame_left, text="Add Record", command=self.add_record)
        self.button_add.pack(pady=(5, 5))

        # Delete Record Button
        self.button_delete = Button(self.frame_left, text="Delete Record", command=self.delete_selected_record)
        self.button_delete.pack(pady=(5, 10))

        # Exit Button (optional)
        self.button_exit = Button(self.frame_left, text="Exit", command=master.quit)
        self.button_exit.pack(pady=(10, 0))
        

        # Desna strana: Tabela sa podacima
        self.frame_right = Frame(master)
        self.frame_right.pack(side='right', fill='both', expand=True)

        self.label_table = Label(self.frame_right, text="Table Records", font=("Arial", 16))
        self.label_table.pack(pady=10)
        
########################################################################################################################################################################################        

    # Filter Label
        self.label_filter = Label(self.frame_right, text="Filter:", font=("Arial", 12))
        self.label_filter.pack(pady=(10, 0))

        # Combobox za filter
        self.filter_combobox = ttk.Combobox(self.frame_right, state='readonly')
        
        self.filter_combobox.pack(pady=(0, 10))
        self.load_titles()

    def load_titles(self):
        """Popunite combobox jedinstvenim naslovima."""
        
        titles = self.db.get_unique_titles()  # Pozivanje funkcije iz Dashboard klase
        if titles:
            self.filter_combobox['values'] = titles  # Popunite combobox sa vrednostima
        else:
            self.filter_combobox['values'] = ["Nema dostupnih naslova"]
            
            ##Treba da se doradi za filter            
######################################################################################################################################################################################## 
        # Treeview za prikaz podataka u tabeli
        self.tree = ttk.Treeview(self.frame_right, columns=("ID", "Title", "Username", "URL", "Password", "Notes"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=0, stretch=tk.NO)
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
        self.context_menu = Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selected_data)        
        self.tree.bind("<Button-3>", self.show_context_menu)    
        self.master.after(100, self.center_window)

    def center_window(self):
        """Centrira prozor na ekranu."""
        width = 1000  # Širina prozora
        height = 750  # Visina prozora
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
            self.tree.insert("", "end", values=(record[0],record[1], record[2], record[3], "******", record[5])) 
    
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
            self.tree.insert("", "end", values=(record[0],record[1], record[2], record[3], password_display, record[5]))        
                
    def add_record(self):
        """Dodajte novi zapis u bazu podataka."""
        title = self.entry_title.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        url = self.entry_url.get()
        notes = self.entry_notes.get("1.0", "end").strip()

        # Proverite da li su svi potrebni podaci uneti
        if title and username and password and url:  # Možete dodati notes ako je potreban
            self.db.add_record(title, username, url, password, notes)
            messagebox.showinfo("Success", "Zapis uspešno dodat!")

            # Resetujte polja nakon dodavanja
            self.entry_title.delete(0, tk.END)  # Ispravljeno
            self.entry_username.delete(0, tk.END)  # Ispravljeno
            self.entry_password.delete(0, tk.END)  # Ispravljeno
            self.entry_url.delete(0, tk.END)  # Ispravljeno
            self.entry_notes.delete("1.0", "end")  # Ispravljeno
            self.load_user_data()  # Osveži tabelu nakon dodavanja
        else:
            messagebox.showwarning("Input Error", "Sva polja moraju biti popunjena!")
    
    def refresh_records_table(self):
        """Osvežava tabelu sa podacima iz baze."""
        # Obrisi sve trenutne redove
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Preuzmi sve zapise iz baze
        records = self.db.get_all_records()  # Pretpostavljamo da imaš metodu za preuzimanje zapisa

        # Dodaj nove redove iz baze
        for record in records:
            self.tree.insert('', 'end', values=record)

    def delete_selected_record(self):
        """Brisanje selektovanog zapisa."""
        selected_item = self.tree.selection()  # Get the selected item in the Treeview
        if selected_item:
            # Get values of the selected row (assuming ID is stored in the first column, adjust as needed)
            record_values = self.tree.item(selected_item, 'values')
            title = record_values[0]  # Adjust based on how you store your values; assuming ID is first value

            # Confirm the deletion
            confirm = messagebox.askyesno("Potvrda", f"Da li ste sigurni da želite da obrišete zapis '{title}'?")
            if confirm:
                # Call the database method to delete the record (use ID or some unique field to delete)
                self.db.delete_record(title)  # Assuming your database method is named delete_record
                
                # Refresh the table
                self.load_user_data()
                messagebox.showinfo("Uspeh", f"Zapis '{title}' je uspešno obrisan.")
        else:
            messagebox.showwarning("Greška", "Nije selektovan zapis za brisanje.")    

    def create_database_gui(self):
        db_path = filedialog.asksaveasfilename(defaultextension=".db",
                                                 filetypes=[("SQLite Database", "*.db")])
        if db_path:
            self.db = Dashboard(db_path)
            #messagebox.showinfo("Status", "Baza podataka uspešno kreirana.")

    def generate_password(self):
        """Generiše nasumičnu lozinku i postavlja je u polje za unos lozinke."""
        password = self.db.generate_random_password()  # Pozivamo metodu iz dashboard.py
        self.entry_password.delete(0, tk.END)  # Očisti prethodni unos
        self.entry_password.insert(0, password)  # Postavi novu lozinku

    def import_data(self):
        print("Import data functionality goes here")

    def export_data(self):        
        db_path = "databases/users_database.db"  # Putanja do tvoje baze podataka
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            exporter = Export(db_path)  
            exporter.export_to_csv(csv_file_path)  
        else:
            messagebox.showinfo("Export Cancelled", "Izvoz podataka je otkazan.")

    def show_about(self):
        messagebox.showinfo("About", "Ovo je dashboard aplikacija.")
        
        
    def show_context_menu(self, event):
        """Prikažite kontekstualni meni pri desnom kliku."""
        try:
            self.tree.selection_set(self.tree.identify_row(event.y))  # Selektujte red na koji je desni klik
            self.context_menu.post(event.x_root, event.y_root)  # Prikažite meni
        except Exception as e:
            print(e)

    def copy_selected_data(self):
        """Kopirajte izabrani tekst iz Treeview u clipboard."""
        selected_item = self.tree.selection()  # Dobijte izabrani red
        if selected_item:  # Proverite da li je red izabran
            item_values = self.tree.item(selected_item, 'values')  # Dobijte vrednosti izabranog reda
            if item_values:
                # Korisnik može izabrati koji element da kopira
                selected_column = self.tree.identify_column(self.tree.winfo_pointerx() - self.tree.winfo_rootx())
                column_index = int(selected_column.replace('#', '')) - 1  # Konvertuj u indeks
                text_to_copy = item_values[column_index]  # Dobijte tekst iz selektovane kolone
                pyperclip.copy(text_to_copy)  # Kopirajte u clipboard
            else:
                # Ova poruka se može zadržati ako želite obavestiti korisnika u slučaju problema
                tk.messagebox.showwarning("Warning", "No data to copy.")
        else:
            # Ova poruka se može zadržati ako želite obavestiti korisnika u slučaju problema
            tk.messagebox.showwarning("Warning", "No item selected.") 
            
    def on_entry_focus_in(self, event):
        event.widget.config(bg='white')  # Promeni pozadinsku boju na belu

    def on_entry_focus_out(self, event):
        event.widget.config(bg='lightgrey')  # Promeni pozadinsku boju na sivu

    def on_text_focus_in(self, event):
        event.widget.config(bg='white')  # Promeni pozadinsku boju na belu

    def on_text_focus_out(self, event):
        event.widget.config(bg='lightgrey')  # Promeni pozadinsku boju na sivu        
           
    def on_close(self):
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    dashboard_window = DashboardWindow(root, user_id=1)
    root.mainloop()
