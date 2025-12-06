import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from components.book_treeview import BookTreeView
from utils import get_all_books, add_book, update_book, get_all_transactions, update_transaction


class ManagerDashboard:
    def __init__(self, root, username, show_login_callback):
        self.root = root
        self.username = username
        self.show_login_callback = show_login_callback
        self.build_header()
        self.create_tabs()

    # ---------------- HEADER W/ LOGOUT ----------------
    def build_header(self):
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")

        ttk.Label(header, text=f"Manager Dashboard - {self.username}", font=("Arial", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Logout", command=self.show_login_callback).pack(side="right")

    # ---------------- TABS ----------------
    def create_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # --- Book List Tab ---
        book_frame = ttk.Frame(notebook, padding=10)
        notebook.add(book_frame, text="Book List")

        columns = ("ID", "Title", "Author", "Buy Price", "Rent Price", "Quantity")
        self.book_tree = BookTreeView(book_frame, columns, double_click_callback=self.on_double_click)

        ttk.Button(book_frame, text="Add New Book", command=self.open_add_book_window).pack(pady=10)

        self.load_books()

        # --- Transaction Tab ---
        transaction_frame = ttk.Frame(notebook, padding=10)
        notebook.add(transaction_frame, text="Transaction List")
        
        ttk.Label(transaction_frame, text="All Transactions", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Transaction tree
        trans_columns = ("ID", "User", "Book", "Author", "Type", "Cost", "Status", "Date")
        self.transaction_tree = ttk.Treeview(transaction_frame, columns=trans_columns, show="headings")
        for col in trans_columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, anchor="center", width=100)
        self.transaction_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Bind double-click to edit transaction
        self.transaction_tree.bind("<Double-1>", self.on_transaction_double_click)

        ttk.Button(transaction_frame, text="Refresh Transactions", command=self.load_transactions).pack(pady=5)
        
        self.load_transactions()

    # ---------------- LOAD BOOKS ----------------
    def load_books(self):
        books = get_all_books()
        self.book_tree.populate(books)

    # ---------------- LOAD TRANSACTIONS ----------------
    def load_transactions(self):
        transactions = get_all_transactions()
        
        # Clear existing
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        # Populate
        for t in transactions:
            # Convert cost to float if it's a string
            cost = t.get('cost', 0)
            try:
                cost_float = float(cost)
            except (ValueError, TypeError):
                cost_float = 0.0
            
            self.transaction_tree.insert("", tk.END, values=(
                t.get("transaction_id"),
                t.get("username"),
                t.get("book_title"),
                t.get("author"),
                t.get("type"),
                f"${cost_float:.2f}",
                t.get("status"),
                str(t.get("created_at", ""))[:19]  # Format timestamp
            ))

    # ---------------- ADD BOOK POPUP ----------------
    def open_add_book_window(self):
        popup = Toplevel(self.root)
        popup.title("Add New Book")
        popup.geometry("350x300")
        popup.resizable(False, False)

        ttk.Label(popup, text="Add Book", font=("Arial", 14, "bold")).pack(pady=10)
        container = ttk.Frame(popup, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        fields = ["Title", "Author", "Buy Price", "Rent Price", "Quantity"]
        entries = {}

        for i, field in enumerate(fields):
            ttk.Label(container, text=field + ":").grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(container)
            entry.grid(row=i, column=1, pady=5)
            entries[field] = entry

        def save_new_book():
            data = {
                "title": entries["Title"].get(),
                "author": entries["Author"].get(),
                "price_buy": entries["Buy Price"].get(),
                "price_rent": entries["Rent Price"].get(),
                "quantity": entries["Quantity"].get()
            }

            if not all(data.values()):
                messagebox.showerror("Error", "All fields must be filled.")
                return

            res, status = add_book(data)
            if status == 201:
                messagebox.showinfo("Success", "Book added successfully")
                popup.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", res.get("error", "Unknown error"))

        ttk.Button(popup, text="Save", command=save_new_book).pack(pady=15)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack()

    # ---------------- EDIT (DOUBLE CLICK) ----------------
    def on_double_click(self, event):
        item_id = self.book_tree.focus()
        if not item_id:
            return
        item = self.book_tree.item(item_id)
        values = item["values"]
        book_id = values[0]
        self.open_edit_book_window(book_id, values)

    # ---------------- EDIT BOOK POPUP ----------------
    def open_edit_book_window(self, book_id, values):
        popup = Toplevel(self.root)
        popup.title("Edit Book")
        popup.geometry("350x350")
        popup.resizable(False, False)

        ttk.Label(popup, text="Edit Book", font=("Arial", 14, "bold")).pack(pady=10)
        container = ttk.Frame(popup, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        labels = ["Title", "Author", "Buy Price", "Rent Price", "Quantity"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(container, text=label + ":").grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(container)
            entry.insert(0, values[i+1])  # skip ID
            entry.grid(row=i, column=1, pady=5)
            entries.append(entry)

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def save_changes():
            data = {
                "title": entries[0].get(),
                "author": entries[1].get(),
                "price_buy": entries[2].get(),
                "price_rent": entries[3].get(),
                "quantity": entries[4].get()
            }

            if not all(data.values()):
                messagebox.showerror("Error", "All fields must be filled.")
                return

            res, status = update_book(book_id, data)
            if status == 200:
                messagebox.showinfo("Success", "Book updated successfully")
                popup.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", res.get("error", "Unknown error"))

        ttk.Button(btn_frame, text="Save", command=save_changes).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=popup.destroy).grid(row=0, column=1, padx=10)

    # ---------------- EDIT TRANSACTION (DOUBLE CLICK) ----------------
    def on_transaction_double_click(self, event):
        item_id = self.transaction_tree.focus()
        if not item_id:
            return
        item = self.transaction_tree.item(item_id)
        values = item["values"]
        transaction_id = values[0]
        self.open_edit_transaction_window(transaction_id, values)

    # ---------------- EDIT TRANSACTION POPUP ----------------
    def open_edit_transaction_window(self, transaction_id, values):
        popup = Toplevel(self.root)
        popup.title("Edit Transaction")
        popup.geometry("400x400")
        popup.resizable(False, False)

        ttk.Label(popup, text="Edit Transaction", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Display transaction info (read-only)
        info_frame = ttk.Frame(popup, padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True)

        labels = ["ID:", "User:", "Book:", "Author:", "Type:", "Cost:"]
        for i, label in enumerate(labels):
            ttk.Label(info_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
            ttk.Label(info_frame, text=str(values[i]), font=("Arial", 10)).grid(row=i, column=1, sticky=tk.W, pady=5, padx=5)

        # Status dropdown (editable)
        ttk.Label(info_frame, text="Status:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        
        status_var = tk.StringVar(value=values[6])  # Current status
        status_combo = ttk.Combobox(info_frame, textvariable=status_var, values=["pending", "paid"], state="readonly", width=15)
        status_combo.grid(row=6, column=1, sticky=tk.W, pady=5, padx=5)

        # Save and Cancel Buttons
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)

        def save_changes():
            new_status = status_var.get()
            
            res, status = update_transaction(transaction_id, {"status": new_status})
            if status == 200:
                messagebox.showinfo("Success", "Transaction updated successfully")
                popup.destroy()
                self.load_transactions()
            else:
                messagebox.showerror("Error", res.get("error", "Unknown error"))

        ttk.Button(btn_frame, text="Save", command=save_changes).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=popup.destroy).grid(row=0, column=1, padx=10)