# controller/sale_window.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tksheet import Sheet

from controller.sale_service import Sale_Service
from view.checkout_window import Checkout_Window
from model import *


class Sale_Window(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        # Basic window setup
        self.title("Sale")
        self.geometry("900x600")
        self.resizable(True, True)

        # ---------- Menu Bar ----------
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        nav_menu = tk.Menu(menubar, tearoff=0)
        if app.staff_role == "admin":
            nav_menu.add_command(label="Book")   # TODO: hook logic later
            nav_menu.add_command(label="Staff")  # TODO: hook logic later
            nav_menu.add_command(label="Sale")   # TODO: hook logic later
            
        nav_menu.add_command(label="Daily Report")   # TODO: hook logic later
        menubar.add_cascade(label="Navigate", menu=nav_menu)

        # ---------- Layout config ----------
        self.columnconfigure(0, weight=1)
        # row 0: info bar
        # row 1: tksheet
        # row 2: bottom form
        self.rowconfigure(1, weight=1)

        # ---------- Top info bar (date + staff name) ----------
        info_frame = ttk.Frame(self, padding=(10, 5))
        info_frame.grid(row=0, column=0, sticky="ew")

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Date time
        today_str = datetime.now().strftime("%Y-%m-%d")
        date_label = ttk.Label(info_frame, text=f"Date: {today_str}")
        date_label.grid(row=0, column=0, sticky="w")

        # Placeholder: try to get from app, else fallback text
        staff_name = getattr(app, "staff_name", "No name")
        staff_label = ttk.Label(info_frame, text=f"Staff: {staff_name}")
        staff_label.grid(row=0, column=1, sticky="e")

        # ---------- Central tksheet area ----------
        sheet_frame = ttk.Frame(self)
        sheet_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 5))

        sheet_frame.rowconfigure(0, weight=1)
        sheet_frame.columnconfigure(0, weight=1)

        self.sheet = Sheet(
            sheet_frame,
            headers=Book_Sale.BOOK_SALE_HEADER,
            data=[],
        )

        # Enable some basic interactions; tweak later if needed
        self.sheet.enable_bindings((
            "single_select",
            "row_select",
            "column_select",
            "drag_select",
            "arrowkeys",
            "right_click_popup_menu",
            "rc_select",
        ))
        self.sheet.grid(row=0, column=0, sticky="nsew")

        # ---------- Bottom form ----------
        form_frame = ttk.Frame(self, padding=(10, 5))
        form_frame.grid(row=2, column=0, sticky="ew")

        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=0)
        form_frame.columnconfigure(3, weight=0)
        form_frame.columnconfigure(4, weight=0)
        form_frame.columnconfigure(5, weight=0)


        # Item dropdown
        ttk.Label(form_frame, text="Item:").grid(row=0, column=0, sticky="w")
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(
            form_frame,
            textvariable=self.item_var,
            state="readonly",
            width=40,
        )
        self.item_combo.grid(row=0, column=1, sticky="ew", padx=(5, 15))

        # Quantity (number input)
        ttk.Label(form_frame, text="Qty:").grid(row=0, column=2, sticky="w")

        self.qty_var = tk.StringVar(value="1")

        vcmd = (self.register(self._validate_qty), "%P")

        self.qty_entry = ttk.Spinbox(
            form_frame,
            from_=1,
            to=1,                      # temporary, will update when item selected
            textvariable=self.qty_var,
            width=5,
            validate="key",
            validatecommand=vcmd,
        )
        self.qty_entry.grid(row=0, column=3, sticky="w", padx=(5, 15))

        # Bind + button
        self.item_combo.bind("<<ComboboxSelected>>", self._on_item_selected)
        
        self.add_btn = ttk.Button(form_frame, text="Add Sale", command=self.on_add_sale)
        self.add_btn.grid(row=0, column=4, sticky="e", padx=(0, 5))

        self.checkout_btn = ttk.Button(form_frame, text="Checkout", command=self.on_checkout)
        self.checkout_btn.grid(row=0, column=5, sticky="e")




        # INITIAL POPULATION OF COMBO
        self._refresh_book_combo()













    def _on_item_selected(self, event=None):
        """Update the qty Spinbox max based on selected book stock."""
        idx = self.item_combo.current()
        if idx < 0:
            return

        book_row = self.book_rows_for_combo[idx]
        stock_str = book_row[6]

        try:
            stock = int(stock_str)
        except (TypeError, ValueError):
            stock = 1

        if stock < 1:
            stock = 1  # avoid 0/negative for the widget

        # Update spinbox max and reset qty to 1
        self.qty_entry.config(to=stock)
        self.qty_var.set("1")
















    def on_add_sale(self):
        # Must have a selected item
        index = self.item_combo.current()
        if index < 0:
            return  # no selection

        # Get the book row corresponding to the selected item
        book_row = self.book_rows_for_combo[index]

        # Get quantity from Spinbox
        qty_str = self.qty_var.get().strip()
        if not qty_str:
            return

        try:
            qty = int(qty_str)
        except ValueError:
            return

        # Clamp qty to stock as extra safety (even though spinbox already validates)
        try:
            stock = int(book_row[6])
        except (TypeError, ValueError):
            stock = 1

        if qty < 1:
            qty = 1
        if qty > stock:
            qty = stock
            self.qty_var.set(str(qty))

        # Use App-level sale state
        current_sale_id = self.app.current_sale_id
        current_book_sale = self.app.current_book_sale

        # Add via service
        updated_book_sale = Sale_Service.add_book_to_current_book_sale(
            current_book_sale,
            book_row,
            qty,
            current_sale_id,
        )

        # Store back on the app
        self.app.current_book_sale = updated_book_sale

        # Refresh the tksheet with the new data
        self.sheet.set_sheet_data(self.app.current_book_sale)

        # Rebuild combobox based on remaining stock
        self._refresh_book_combo()















    def _validate_qty(self, proposed: str) -> bool:
        """
        Spinbox validation callback.
        `proposed` is the would-be new value of the entry (%P).
        Returns True if allowed, False to reject the keypress.
        """
        # Allow empty while user is typing
        if proposed == "":
            return True

        # Must be all digits
        if not proposed.isdigit():
            return False

        # Must be >= 1
        return int(proposed) >= 1
    











    def _refresh_book_combo(self):
        """
        Rebuilds the list of books for the combobox based on the
        remaining stock after current_book_sale.
        """
        # Ask service for a *fresh* view of remaining stock
        book_rows = Sale_Service.get_book_for_display(self.app.current_book_sale)
        self.book_rows_for_combo = book_rows

        book_display_values = [
            f"{row[0]} - {row[1]} (RM {row[5]}, stock {row[6]})"
            for row in book_rows
        ]

        # Update combobox values
        self.item_combo["values"] = book_display_values

        # If nothing left, clear selection and disable qty
        if not book_rows:
            self.item_var.set("")
            self.item_combo.set("")
            self.qty_var.set("1")
            self.qty_entry.config(state="disabled", to=1)
            return

        # Ensure qty is enabled
        self.qty_entry.config(state="normal")
        # Clear selection so user must pick again (avoids stale index)
        self.item_var.set("")
        self.item_combo.set("")
        self.qty_var.set("1")









    def on_checkout(self):
        # Prevent checkout if no items
        if not self.app.current_book_sale:
            return

        Checkout_Window(self.app)
