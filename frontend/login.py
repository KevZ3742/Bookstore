import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:5000"

class LoginRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore - Login & Register")
        self.root.geometry("400x300")
        self.show_login()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # login
    def login_user(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        try:
            res = requests.post(
                f"{API_URL}/auth/login",
                json={"username": username, "password": password}
            )
            data = res.json()
        except Exception:
            messagebox.showerror("Error", "Cannot reach server.")
            return

        if data["status"] == "success":
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login Failed", data.get("message", "Error"))
    
    def show_login(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=1, column=1, sticky=tk.EW, padx=10)
        
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=2, column=1, sticky=tk.EW, padx=10)
        
        ttk.Button(
            frame,
            text="Login",
            command=lambda: self.login_user(username_entry, password_entry)
        ).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Need an account?", command=self.show_register).grid(row=4, column=0, columnspan=2)
        
        frame.columnconfigure(1, weight=1)
    
    # register
    def register_user(self, username_entry, email_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Fill all fields.")
            return

        try:
            res = requests.post(
                f"{API_URL}/auth/register",
                json={"username": username, "password": password}
            )
            data = res.json()
        except Exception:
            messagebox.showerror("Error", "Cannot reach server.")
            return
        
        if data["status"] == "success":
            messagebox.showinfo("Register", "Registration successful. Log in now.")
            self.show_login()
        else:
            messagebox.showerror("Registration Failed", data.get("message", "Error"))
    
    def show_register(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
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
        
        ttk.Button(
            frame,
            text="Register",
            command=lambda: self.register_user(username_entry, email_entry, password_entry)
        ).grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Have an account?", command=self.show_login).grid(row=5, column=0, columnspan=2)
        
        frame.columnconfigure(1, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginRegisterApp(root)
    root.mainloop()