import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import requests

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

        # Header with role and logout
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill=tk.X)
        ttk.Label(header, text=f"Logged in as: {self.role}", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(header, text="Logout", command=self.logout).pack(side=tk.RIGHT)

        if self.role == "manager":
            self.create_manager_tabs()
        else:
            frame = ttk.Frame(self.root, padding=20)
            frame.pack(expand=True)
            ttk.Label(frame, text="Customer Dashboard (Coming Soon)", font=("Arial", 16)).pack(pady=20)

    # ---------------- Manager Tabs ----------------
    def create_manager_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # --- Book List Tab ---
        book_frame = ttk.Frame(notebook, padding=10)
        notebook.add(book_frame, text="Book List")

        # TreeView for books
        columns = ("ID", "Title", "Author", "Buy Price", "Rent Price", "Quantity")
        self.book_tree = ttk.Treeview(book_frame, columns=columns, show="headings")
        for col in columns:
            self.book_tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview(self.book_tree, _col, False))
            self.book_tree.column(col, anchor=tk.CENTER, width=120)
        self.book_tree.pack(expand=True, fill=tk.BOTH)

        # Double-click to edit
        self.book_tree.bind("<Double-1>", self.on_double_click)

        # Add Book Button
        ttk.Button(book_frame, text="Add New Book", command=self.open_add_book_window).pack(pady=10)

        # Load initial books
        self.load_books()

        # --- Transaction Tab ---
        transaction_frame = ttk.Frame(notebook, padding=10)
        notebook.add(transaction_frame, text="Transaction List")
        ttk.Label(transaction_frame, text="Transactions will appear here", font=("Arial", 12)).pack(pady=20)

    # ---------------- Load Books ----------------
    def load_books(self):
        try:
            response = requests.get("http://127.0.0.1:5000/books/all")
            if response.status_code != 200:
                messagebox.showerror("Error", "Failed to load books")
                return

            books = response.json()
            # Clear TreeView
            for item in self.book_tree.get_children():
                self.book_tree.delete(item)
            # Insert books
            for b in books:
                self.book_tree.insert(
                    "",
                    tk.END,
                    values=(b["book_id"], b["title"], b["author"], b["price_buy"], b["price_rent"], b["quantity"])
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- Sort TreeView ----------------
    def sort_treeview(self, tree, col, reverse):
        data_list = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            data_list.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data_list.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(data_list):
            tree.move(k, '', index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))

    # ---------------- Add Book Popup ----------------
    def open_add_book_window(self):
        popup = Toplevel(self.root)
        popup.title("Add New Book")
        popup.geometry("350x300")
        popup.resizable(False, False)

        ttk.Label(popup, text="Add Book", font=("Arial", 14, "bold")).pack(pady=10)
        container = ttk.Frame(popup, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Fields
        ttk.Label(container, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(container)
        title_entry.grid(row=0, column=1, pady=5)

        ttk.Label(container, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5)
        author_entry = ttk.Entry(container)
        author_entry.grid(row=1, column=1, pady=5)

        ttk.Label(container, text="Buy Price:").grid(row=2, column=0, sticky=tk.W, pady=5)
        buy_price_entry = ttk.Entry(container)
        buy_price_entry.grid(row=2, column=1, pady=5)

        ttk.Label(container, text="Rent Price:").grid(row=3, column=0, sticky=tk.W, pady=5)
        rent_price_entry = ttk.Entry(container)
        rent_price_entry.grid(row=3, column=1, pady=5)

        ttk.Label(container, text="Quantity:").grid(row=4, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(container)
        quantity_entry.grid(row=4, column=1, pady=5)

        # Submit
        def submit_book():
            data = {
                "title": title_entry.get(),
                "author": author_entry.get(),
                "price_buy": buy_price_entry.get(),
                "price_rent": rent_price_entry.get(),
                "quantity": quantity_entry.get()
            }
            if not all(data.values()):
                messagebox.showerror("Error", "All fields must be filled.")
                return
            try:
                response = requests.post("http://127.0.0.1:5000/books/add", json=data)
                r = response.json()
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Book added successfully")
                    popup.destroy()
                    self.load_books()
                else:
                    messagebox.showerror("Error", r.get("error", "Unknown error"))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(popup, text="Add Book", command=submit_book).pack(pady=15)

    # ---------------- Edit Book Popup ----------------
    def on_double_click(self, event):
        item_id = self.book_tree.focus()
        if not item_id:
            return
        item = self.book_tree.item(item_id)
        values = item["values"]
        book_id = values[0]
        self.open_edit_book_window(book_id, values)

    def open_edit_book_window(self, book_id, values):
        popup = Toplevel(self.root)
        popup.title("Edit Book")
        popup.geometry("350x300")
        popup.resizable(False, False)

        ttk.Label(popup, text="Edit Book", font=("Arial", 14, "bold")).pack(pady=10)
        container = ttk.Frame(popup, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        labels = ["Title", "Author", "Buy Price", "Rent Price", "Quantity"]
        entries = []
        for i, label in enumerate(labels):
            ttk.Label(container, text=label+":").grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(container)
            entry.insert(0, values[i+1])  # skip book_id
            entry.grid(row=i, column=1, pady=5)
            entries.append(entry)

        def submit_edit():
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
            try:
                response = requests.put(f"http://127.0.0.1:5000/books/update/{book_id}", json=data)
                r = response.json()
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Book updated successfully")
                    popup.destroy()
                    self.load_books()
                else:
                    messagebox.showerror("Error", r.get("error", "Unknown error"))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(popup, text="Update Book", command=submit_edit).pack(pady=15)

    # ---------------- Logout ----------------
    def logout(self):
        self.show_login_callback()
