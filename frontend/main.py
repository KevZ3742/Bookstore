import tkinter as tk
from login import LoginRegisterScreen
from dashboard import Dashboard

root = tk.Tk()
root.title("Bookstore App")
root.geometry("400x300")

login_screen = None

def show_login():
    global login_screen
    login_screen = LoginRegisterScreen(root, show_dashboard)

def show_dashboard(role):
    Dashboard(root, role, show_login)

login_screen = LoginRegisterScreen(root, show_dashboard)

root.mainloop()
