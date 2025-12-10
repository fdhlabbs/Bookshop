# controller/book_window.py
import tkinter as tk
from tkinter import ttk
from tksheet import Sheet
import copy
from controller.debug import Debug

from model.book import Book
from controller.uuid_service import Uuid_Service


class Book_Window(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        self.title("Book Management")
        self.geometry("900x500")
        self.resizable(True, True)

        # allow main frame to expand with window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # ---- local working copy ----
        self.book_model = Book()
        self.local_rows = copy.deepcopy(self.book_model.table)

        # ---- Layout ----
        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        # ---- Sheet ----
        self.sheet = Sheet(
            main,
            headers=Book.BOOK_HEADER,
            data=self.local_rows,
        )

        self.sheet.enable_bindings((
            "single_select",
            "row_select",
            "column_select",
            "drag_select",
            "arrowkeys",
            "right_click_popup_menu",
            "rc_select",
            "edit_cell",
            "delete_rows",
            "insert_row",
        ))

        self.sheet.grid(row=0, column=0, sticky="nsew")

        # Make book_id column (index 0) read-only
        self.sheet.readonly_columns([0])

        # Hook row insertion to auto-generate UUID
        self.sheet.bind("<<RowInserted>>", self._on_row_inserted)

        # ---- Bottom bar ----
        bottom = ttk.Frame(main)
        bottom.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=0)

        # Spacer / dummy label so button sits on the right
        ttk.Label(bottom, text="").grid(row=0, column=0, sticky="w")

        # Save & Close button
        ttk.Button(
            bottom,
            text="Save and Close",
            command=self.on_save_and_close,
        ).grid(row=0, column=1, sticky="e")

    # ------------------------------------------------------------
    # Event: New row inserted → auto-generate book_id
    # ------------------------------------------------------------

    def _on_row_inserted(self, event=None):
        Debug.print("_on_row_inserted", "event", "1")
        selected = self.sheet.get_selected_rows()
        if not selected:
            return

        row_index = selected[0]

        new_id = Uuid_Service.new_id()
        self.sheet.set_cell_data(row_index, 0, new_id)

    # ------------------------------------------------------------
    # Save (no validation)
    # ------------------------------------------------------------

    def on_save_and_close(self):
        # Just grab whatever is in the sheet and save it back
        rows = self.sheet.get_sheet_data()
        self.book_model.table = rows
        self.destroy()
