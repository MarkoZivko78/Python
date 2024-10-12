import tkinter as tk
from gui.gui_login import LoginWindow  # Uvezi LoginWindow klasu
from tkinter import PhotoImage

class App(tk.Tk):
    def __init__(self):
        super().__init__()  # Inicijalizacija Tkinter klase
        self.title("NMD Secure")  # Postavi naslov prozora
        self.geometry("400x300")  # Postavi dimenzije prozora

        # Postavi ikonu za taskbar
        self.iconbitmap('icons/icon.ico')  # Putanja do .ico ikone

        # Učitavanje ikona (npr. za dugmad)
        self.icon1 = PhotoImage(file='icons/ico.png')  # Putanja do prve ikone
        
        self.login_gui = LoginWindow(self)  # Prosledi self kao master
        
    def on_close(self):
        """Zatvaranje GUI-a."""        
        self.quit()  # Završava mainloop
        self.destroy()  # Zatvara prozor 
        
if __name__ == "__main__":
    app = App()  # Kreiraj instancu glavne aplikacije
    app.mainloop()  # Pokreni glavnu petlju
