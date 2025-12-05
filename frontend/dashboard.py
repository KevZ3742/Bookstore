import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, root, role, show_login_callback):
        self.root = root
        self.role = role
        self.show_login_callback = show_login_callback
        self.show_dashboard()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=f"Logged in as: {self.role}", font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Button(frame, text="Logout", command=self.logout).pack(pady=10)

    def logout(self):
        self.show_login_callback()