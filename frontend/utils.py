import requests
from tkinter import messagebox

API_URL = "http://127.0.0.1:5000"

def login_user(username, password):
    try:
        res = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        return res.json()
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"status": "fail", "message": "Server not reachable"}

def register_user(username, password):
    try:
        res = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
        return res.json()
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"status": "fail", "message": "Server not reachable"}