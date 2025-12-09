# controller/app.py
import tkinter as tk
import tksheet as tks
from model import *
from view import *
from controller.uuid_service import Uuid_Service

class App:
    def __init__(self, root):
        self.root = root

        # Hide root until login succeeds
        self.root.withdraw()

        # Initialize Database
        db=Database()

        # Initialize Models
        Book(db.book)
        Book_Sale(db.book_sale)
        Sale(db.sale)
        Staff(db.staff)

        # --- Show Login ---
        login = Login_Window(self)

        # Block here until Login is closed
        self.root.wait_window(login)

        # --- After Login closes ---
        if getattr(login, "authenticated", False) is False:
            # Login failed or user closed window
            self.root.destroy()
            return

        # --- Login succeeded ---
        self.staff_id = login.staff_id
        self.staff_name = login.staff_name
        self.staff_role = login.staff_role

        # Show main app window
        self.root.deiconify()
        self.current_book_sale = []
        self.current_sale_id = Uuid_Service.new_id()
        sale = Sale_Window(self)


