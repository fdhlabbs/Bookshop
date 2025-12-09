# controller/login_window.py
import tkinter as tk
from tkinter import ttk
from controller.auth_service import Auth_Service


class Login_Window(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)

        self.title("Login")
        self.geometry("300x180")
        self.resizable(False, False)

        # Username
        username_label = ttk.Label(self, text="Username:")
        username_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))

        self.username_entry = ttk.Entry(self, width=25)
        self.username_entry.grid(row=0, column=1, pady=(0, 5))

        # Password
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(0, 5))

        self.password_entry = ttk.Entry(self, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=(0, 5))

        # Error label (hidden by default)
        self.error_label = ttk.Label(self, text="", foreground="red")

        # Login button
        self.login_try_count = 0
        self.authenticated = False
        self.role = None
        login_button = ttk.Button(self, text="Login", command=self.on_login)
        self.bind("<Return>", lambda event: self.on_login())
        login_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        # Make columns resize nicely
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)






    def show_error(self, message: str):
        self.error_label.config(text=message)

        # If not yet visible, place it under the password row
        if not self.error_label.winfo_ismapped():
            self.error_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))






    def clear_error(self):
        if self.error_label.winfo_ismapped():
            self.error_label.grid_remove()






    def on_login(self):
        # Lock-out check first
        if self.login_try_count >= 3:
            self.show_error("Too many failed attempts. Please try again later.")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        self.clear_error()

        # Empty form
        if not username or not password:
            self.show_error("Username and password are required.")
            return

        username_exist, password_correct, staff_id, staff_name, staff_role = Auth_Service.authenticate(username, password)

        if not username_exist:
            self.login_try_count += 1
            self.show_error("Username does not exist.")

        elif not password_correct:
            self.login_try_count += 1
            self.show_error("Incorrect password.")

        else:
            # Success
            self.authenticated = True
            self.staff_id = staff_id
            self.staff_name = staff_name
            self.staff_role = staff_role
            self.destroy()