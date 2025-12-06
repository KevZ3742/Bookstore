import tkinter as tk
from tkinter import ttk, messagebox
from utils import checkout_order

class Cart:
    def __init__(self, parent, user_id=None, on_checkout_callback=None):
        self.parent = parent
        self.user_id = user_id
        self.on_checkout_callback = on_checkout_callback
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        # Tree
        self.tree = ttk.Treeview(self.frame, columns=("Title", "Author", "Type", "Cost"), show="headings", selectmode="browse")
        for col in ("Title", "Author", "Type", "Cost"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(expand=True, fill="both", padx=5, pady=(5,0))

        # Controls row: Remove & Checkout
        controls = ttk.Frame(self.frame)
        controls.pack(fill="x", pady=8, padx=5)

        self.remove_btn = ttk.Button(controls, text="Remove Selected", command=self.remove_selected)
        self.remove_btn.pack(side="left")

        self.checkout_btn = ttk.Button(controls, text="Checkout", command=self.checkout)
        self.checkout_btn.pack(side="right")

        # Total label
        self.total_label = ttk.Label(self.frame, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=(0,8))

        # data
        self.items = []
        self.refresh()

    def add_item(self, title, author, type_choice, cost):
        """Add an item to the cart and refresh the view."""
        try:
            cost_val = float(cost)
        except Exception:
            try:
                cost_val = float(str(cost).replace("$", "").replace(",", ""))
            except Exception:
                messagebox.showerror("Error", "Invalid cost value")
                return

        self.items.append({
            "title": title,
            "author": author,
            "type": type_choice,
            "cost": cost_val
        })
        self.refresh()

    def refresh(self):
        # clear
        for item in self.tree.get_children():
            self.tree.delete(item)

        total = 0.0
        for entry in self.items:
            self.tree.insert("", tk.END, values=(entry["title"], entry["author"], entry["type"], f"${entry['cost']:.2f}"))
            total += entry["cost"]

        self.total_label.config(text=f"Total: ${total:.2f}")

        # disable remove/checkout if empty
        if len(self.items) == 0:
            self.remove_btn.state(["disabled"])
            self.checkout_btn.state(["disabled"])
        else:
            self.remove_btn.state(["!disabled"])
            self.checkout_btn.state(["!disabled"])

    def remove_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Remove", "No item selected to remove.")
            return
        idx = self.tree.index(sel[0])
        # confirm
        if not messagebox.askyesno("Remove", "Remove selected item from cart?"):
            return
        # remove from data and refresh
        try:
            del self.items[idx]
        except Exception:
            # fallback: try to find matching by values
            vals = self.tree.item(sel[0])["values"]
            for i, it in enumerate(self.items):
                if (it["title"], it["author"], it["type"], f"${it['cost']:.2f}") == tuple(vals):
                    del self.items[i]
                    break
        self.refresh()

    def checkout(self):
        if not self.items:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return

        if not self.user_id:
            messagebox.showerror("Error", "User not logged in.")
            return

        total = sum(it["cost"] for it in self.items)
        confirm = messagebox.askyesno("Checkout", f"Confirm checkout? Total: ${total:.2f}")
        if not confirm:
            return

        # Call backend checkout
        res, status = checkout_order(self.user_id, self.items)
        
        if status == 201:
            # Show detailed message
            message = res.get("message", "Checkout successful!")
            pending_items = res.get("pending_items", [])
            
            if pending_items:
                message += f"\n\nPending items (out of stock):\n" + "\n".join(f"- {item}" for item in pending_items)
                message += "\n\nThese will be fulfilled when back in stock."
            
            messagebox.showinfo("Checkout Complete", message)
            self.items = []
            self.refresh()
            
            # Call the callback to refresh transactions if provided
            if self.on_checkout_callback:
                self.on_checkout_callback()
        else:
            messagebox.showerror("Checkout Failed", res.get("error", "Unknown error occurred"))