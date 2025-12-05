import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from components.book_treeview import BookTreeView
from components.cart import Cart
from utils import get_all_books

class CustomerDashboard:
    def __init__(self, root, show_login_callback):
        self.root = root
        self.show_login_callback = show_login_callback
        self.build_header()
        self.create_tabs()

    # ---------------- HEADER ----------------
    def build_header(self):
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")

        ttk.Label(header, text="Customer Dashboard", font=("Arial", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Logout", command=self.show_login_callback).pack(side="right")

    # ---------------- TABS ----------------
    def create_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Book List Tab ---
        book_frame = ttk.Frame(notebook, padding=10)
        notebook.add(book_frame, text="Book List")

        # Search bar
        search_frame = ttk.Frame(book_frame)
        search_frame.pack(fill="x", pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side="left", padx=5)

        columns = ("ID", "Title", "Author", "Buy Price", "Rent Price", "Quantity")
        self.book_tree = BookTreeView(book_frame, columns, double_click_callback=self.on_book_double_click)

        # Load books initially
        self.load_books()

        # --- Cart Tab ---
        cart_frame = ttk.Frame(notebook, padding=10)
        notebook.add(cart_frame, text="Shopping Cart")

        self.cart = Cart(cart_frame)

    # ---------------- LOAD BOOKS ----------------
    def load_books(self, keyword=None):
        books = get_all_books()
        if keyword:
            keyword = keyword.lower()
            books = [b for b in books if keyword in b["title"].lower() or keyword in b["author"].lower()]
        self.book_tree.populate(books)

    def search_books(self):
        keyword = self.search_entry.get()
        self.load_books(keyword)

    # ---------------- Double click handler that shows Buy/Rent/Cancel popup ----------------
    def on_book_double_click(self, event):
        """
        When a customer double-clicks a book, show a small popup with three choices:
        Buy | Rent | Cancel
        """
        item_id = self.book_tree.focus()
        if not item_id:
            return
        item = self.book_tree.item(item_id)
        values = item["values"]

        title = values[1]
        author = values[2]
        # ensure prices are floats (if backend returns strings)
        try:
            buy_price = float(values[3])
        except Exception:
            buy_price = float(str(values[3]).replace("$", "").replace(",", ""))

        try:
            rent_price = float(values[4])
        except Exception:
            rent_price = float(str(values[4]).replace("$", "").replace(",", ""))

        # Create the small choice popup
        popup = Toplevel(self.root)
        popup.title("Add to Cart")
        popup.geometry("320x150")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()  # modal

        ttk.Label(popup, text=f"Add '{title}' to cart?", font=("Arial", 12, "bold")).pack(pady=(10,5))
        ttk.Label(popup, text=f"Author: {author}").pack()

        # Price labels
        price_frame = ttk.Frame(popup)
        price_frame.pack(pady=8)
        ttk.Label(price_frame, text=f"Buy: ${buy_price:.2f}").grid(row=0, column=0, padx=10)
        ttk.Label(price_frame, text=f"Rent: ${rent_price:.2f}").grid(row=0, column=1, padx=10)

        # Button row
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=8)

        def choose_buy():
            self.cart.add_item(title, author, "Buy", buy_price)
            popup.destroy()

        def choose_rent():
            self.cart.add_item(title, author, "Rent", rent_price)
            popup.destroy()

        def choose_cancel():
            popup.destroy()

        ttk.Button(btn_frame, text="Buy", command=choose_buy).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="Rent", command=choose_rent).grid(row=0, column=1, padx=8)
        ttk.Button(btn_frame, text="Cancel", command=choose_cancel).grid(row=0, column=2, padx=8)
