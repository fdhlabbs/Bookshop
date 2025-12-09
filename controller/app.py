# controller/app.py
import tkinter as tk
import tksheet as tks
from model import *
from view import *

class App:
    def __init__(self, root):
        self.root = root

        # Hide root until login succeeds
        self.root.withdraw()

        # Initialize Database
        db = Database()

        # Initialize Models
        Book(db.book)
        Book_Sale(db.book_sale)
        Sale(db.sale)
        Staff(db.staff)

        # --- Show Login ---
        login = Login_Window(self)
        self.root.wait_window(login)

        if getattr(login, "authenticated", False) is False:
            self.root.destroy()
            return

        self.staff_id = login.staff_id
        self.staff_name = login.staff_name
        self.staff_role = login.staff_role

        # Show main app window
        self.root.deiconify()

        # ---- sale state ----
        self.current_book_sale = []
        self.current_sale = {}  # will be filled at checkout

        sale = Sale_Window(self)
