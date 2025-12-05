from tkinter import ttk
from components.manager_dashboard import ManagerDashboard
from components.customer_dashboard import CustomerDashboard

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
        if self.role == "manager":
            ManagerDashboard(self.root, self.show_login_callback)
        else:
            CustomerDashboard(self.root, self.show_login_callback)
