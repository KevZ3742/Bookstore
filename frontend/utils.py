import requests
from tkinter import messagebox

API_URL = "http://127.0.0.1:5000"

# auth
def login_user(username, password):
    try:
        res = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        return res.json()
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"status": "fail", "message": "Server not reachable"}

def register_user(username, email, password):
    try:
        res = requests.post(f"{API_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        return res.json()
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"status": "fail", "message": "Server not reachable"}

# books
def get_all_books():
    try:
        res = requests.get(f"{API_URL}/books/all")
        return res.json() if res.status_code == 200 else []
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return []

def add_book(data):
    try:
        res = requests.post(f"{API_URL}/books/add", json=data)
        return res.json(), res.status_code
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"error": "Server not reachable"}, 500

def update_book(book_id, data):
    try:
        res = requests.put(f"{API_URL}/books/update/{book_id}", json=data)
        return res.json(), res.status_code
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"error": "Server not reachable"}, 500

# transactions
def checkout_order(user_id, items):
    """
    items: list of dicts with keys: title, author, type, cost
    """
    try:
        res = requests.post(f"{API_URL}/transactions/checkout", json={
            "user_id": user_id,
            "items": items
        })
        return res.json(), res.status_code
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"error": "Server not reachable"}, 500

def get_all_transactions():
    """Get all transactions (for manager)."""
    try:
        res = requests.get(f"{API_URL}/transactions/all")
        return res.json() if res.status_code == 200 else []
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return []

def get_user_transactions(user_id):
    """Get transactions for a specific user."""
    try:
        res = requests.get(f"{API_URL}/transactions/user/{user_id}")
        return res.json() if res.status_code == 200 else []
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return []

def update_transaction(transaction_id, data):
    """Update a transaction."""
    try:
        res = requests.put(f"{API_URL}/transactions/update/{transaction_id}", json=data)
        return res.json(), res.status_code
    except Exception:
        messagebox.showerror("Error", "Cannot reach server.")
        return {"error": "Server not reachable"}, 500