import tkinter as tk
from tkinter import ttk, messagebox
from dashboard import Dashboard
import utils

class LoginRegisterScreen:
    def __init__(self, root, show_dashboard_callback):
        self.root = root
        self.show_dashboard_callback = show_dashboard_callback
        self.show_login()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=1, column=1, sticky=tk.EW, padx=10)

        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=2, column=1, sticky=tk.EW, padx=10)

        ttk.Button(frame, text="Login",
                   command=lambda: self.handle_login(username_entry, password_entry)).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame, text="Need an account?", command=self.show_register).grid(row=4, column=0, columnspan=2)
        frame.columnconfigure(1, weight=1)

    def handle_login(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()
        res = utils.login_user(username, password)
        if res["status"] == "success":
            user_info = {
                "role": res["role"],
                "user_id": res["user_id"],
                "username": res["username"]
            }
            self.show_dashboard_callback(user_info)
        else:
            messagebox.showerror("Login Failed", res.get("message", "Error"))

    def show_register(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Register", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=1, column=1, sticky=tk.EW, padx=10)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(frame)
        email_entry.grid(row=2, column=1, sticky=tk.EW, padx=10)

        ttk.Label(frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=3, column=1, sticky=tk.EW, padx=10)

        ttk.Button(frame, text="Register",
                   command=lambda: self.handle_register(username_entry, email_entry, password_entry)).grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Have an account?", command=self.show_login).grid(row=5, column=0, columnspan=2)
        frame.columnconfigure(1, weight=1)

    def handle_register(self, username_entry, email_entry, password_entry):
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        res = utils.register_user(username, email, password)
        if res["status"] == "success":
            messagebox.showinfo("Register", "Registration successful! Please login.")
            self.show_login()
        else:
            messagebox.showerror("Register Failed", res.get("message", "Error"))