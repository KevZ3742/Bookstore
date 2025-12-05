import tkinter as tk
from tkinter import ttk

class BookTreeView(ttk.Treeview):
    def __init__(self, parent, columns, double_click_callback=None):
        super().__init__(parent, columns=columns, show="headings")
        for col in columns:
            self.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))
            self.column(col, anchor=tk.CENTER, width=120)
        self.pack(expand=True, fill=tk.BOTH)
        if double_click_callback:
            self.bind("<Double-1>", double_click_callback)

    def populate(self, books):
        for item in self.get_children():
            self.delete(item)
        for b in books:
            self.insert("", tk.END, values=(b.get("book_id"), b.get("title"), b.get("author"),
                                            b.get("price_buy"), b.get("price_rent"), b.get("quantity")))

    def sort_column(self, col, reverse):
        data_list = [(self.set(k, col), k) for k in self.get_children('')]
        try:
            data_list.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data_list.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(data_list):
            self.move(k, '', index)
        self.heading(col, command=lambda: self.sort_column(col, not reverse))
