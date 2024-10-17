import tkinter as tk
from tkinter import messagebox
from gui.gui_register import RegisterWindow  # Uvezi RegisterWindow
from gui.gui_dashboard import DashboardWindow
from backend.login import LoginHandler

class LoginWindow:
    
    
    def __init__(self, master):
        super().__init__()  # Inicijalizuj Tk
        self.master = master
        master.title("Login")
        
        master.geometry("250x250")
        master.eval('tk::PlaceWindow %s center' % master.winfo_toplevel())

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.pack()

        self.button_login = tk.Button(master, text="Log In", command=self.login)
        self.button_login.pack(pady=10)
        
        # Dugme za registraciju koje otvara RegisterWindow
        self.button_register = tk.Button(master, text="Register", command=self.open_register_window)
        self.button_register.pack(pady=20)
        
        # Inicijalizacija LoginHandler
        self.login_handler = LoginHandler()
        
        # Povezivanje zatvaranja prozora sa on_close metodom
        master.protocol("WM_DELETE_WINDOW", self.on_close)
    
      

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = self.login_handler.authenticate(username, password)  # Pozovi authenticate metodu
        if user:
            user_id, username = user
            messagebox.showinfo("Uspeh", f"Uspešna prijava kao {username}!")
            self.open_dashboard(user_id)
        else:
            messagebox.showerror("Greška", "Pogrešno korisničko ime ili lozinka.")
            
    def open_dashboard(self, user_id):
        self.master.withdraw()  # Sakrij login prozor
        dashboard_root = tk.Toplevel(self.master)
        DashboardWindow(dashboard_root, user_id)  # Prosledi user_i       

    def open_register_window(self):
        self.master.withdraw()  # Sakrij login prozor
        register_root = tk.Toplevel(self.master)
        RegisterWindow(register_root)
        
    def on_close(self):
        """Zatvaranje GUI-a."""
        self.master.quit()  # Završava mainloop
        self.master.destroy()  # Zatvara prozor      
    
    
    def onlogin(self,event):
        self.login
   

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()    
    