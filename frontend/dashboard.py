from tkinter import ttk
from components.manager_dashboard import ManagerDashboard
from components.customer_dashboard import CustomerDashboard

class Dashboard:
    def __init__(self, root, user_info, show_login_callback):
        self.root = root
        self.user_info = user_info
        self.show_login_callback = show_login_callback
        self.show_dashboard()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_frame()
        role = self.user_info.get("role")
        username = self.user_info.get("username")
        user_id = self.user_info.get("user_id")
        
        if role == "manager":
            ManagerDashboard(self.root, username, self.show_login_callback)
        else:
            CustomerDashboard(self.root, user_id, username, self.show_login_callback)