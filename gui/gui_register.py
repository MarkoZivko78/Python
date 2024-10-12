import tkinter as tk
from tkinter import messagebox
from backend.register import register_user
from backend.user_database import UserDatabase


class RegisterWindow:
    
    
    def center_window(self, window):
        window.update_idletasks()
        width = 400
        height = 400
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")    
        
    def __init__(self, master):
        
        self.db = UserDatabase(db_file='databases/users_database.db')
        
        self.master = master
        master.title("Register")

        self.center_window(master)

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(master)
        self.entry_username.pack(pady=10)

        self.label_email = tk.Label(master, text="Email:")
        self.label_email.pack(pady=10)

        self.entry_email = tk.Entry(master)
        self.entry_email.pack(pady=10)

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.pack(pady=10)

        self.label_confirm_password = tk.Label(master, text="Confirm Password:")
        self.label_confirm_password.pack(pady=10)

        self.entry_confirm_password = tk.Entry(master, show='*')
        self.entry_confirm_password.pack(pady=10)

        self.button_register = tk.Button(master, text="Register", command=self.register)
        self.button_register.pack(pady=10)

        self.button_back_login = tk.Button(master, text="Back to Login", command=self.back_to_login)
        self.button_back_login.pack()  # Ispravka u komentaru

        # Povezivanje metode za zatvaranje prozora
        master.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def back_to_login(self):
        from gui.gui_login import LoginWindow  # Premesti import ovde
        self.master.destroy()  # Zatvori trenutni prozor za registraciju
        login_root = tk.Tk()  # Kreiraj novi prozor za login
        LoginWindow(login_root)  # Kreiraj novu instancu LoginWindow
        login_root.mainloop()  # Pokreni glavnu petlju 
        
    def open_register_window(self):
        self.master.withdraw()  # Sakrij login prozor
        register_root = tk.Toplevel(self.master)
        RegisterWindow(register_root)    

    def register(self):
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        # Poziv register_user funkcije
        success, message = register_user(username, email, password, confirm_password)

        if not success:
            messagebox.showerror("Greška", message)
        else:
            messagebox.showinfo("Uspeh", message)
    
    def on_close(self):
        """Zatvaranje GUI-a."""
        self.master.quit()  # Završava mainloop
        self.master.destroy()  # Zatvara prozor      
            
if __name__ == "__main__":
    root = tk.Tk()
    register_window = RegisterWindow(root)
    root.mainloop()        