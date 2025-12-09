# view/checkout_window.py
import tkinter as tk
from tkinter import ttk
from controller.sale_service import Sale_Service
from controller.uuid_service import Uuid_Service


class Checkout_Window(tk.Toplevel):

    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        self.title("Checkout")
        self.geometry("400x350")
        self.resizable(False, False)

        # ----- internal state -----
        self.subtotal_value = self._compute_subtotal()
        self.discount_rate = 0.0
        self.discount_value = 0.0

        # base values BEFORE any voucher
        self.tax_value = self.subtotal_value * Sale_Service.TAX_RATE
        self.total_value = self.subtotal_value + self.tax_value
        self.balance_value = 0.0

        # ----- StringVars for display -----
        self.staff_name_var = tk.StringVar(
            value=getattr(app, "staff_name", "Unknown")
        )
        self.subtotal_var = tk.StringVar(value=f"{self.subtotal_value:.2f}")
        self.discount_code_var = tk.StringVar()
        self.discount_msg_var = tk.StringVar(value="")  # hidden (empty) initially
        self.discount_var = tk.StringVar(value=f"{self.discount_value:.2f}")
        self.tax_var = tk.StringVar(value=f"{self.tax_value:.2f}")
        self.total_var = tk.StringVar(value=f"{self.total_value:.2f}")
        self.cash_received_var = tk.StringVar()
        self.balance_var = tk.StringVar(value=f"{self.balance_value:.2f}")

        # ----- Layout -----
        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        for i in range(2):
            main.columnconfigure(i, weight=1)

        row = 0

        # Staff name
        ttk.Label(main, text="Staff name:").grid(row=row, column=0, sticky="w")
        ttk.Label(main, textvariable=self.staff_name_var).grid(
            row=row, column=1, sticky="w"
        )
        row += 1

        # Subtotal
        ttk.Label(main, text="Subtotal (RM):").grid(row=row, column=0, sticky="w")
        ttk.Label(main, textvariable=self.subtotal_var).grid(
            row=row, column=1, sticky="w"
        )
        row += 1

        # Discount voucher input
        ttk.Label(main, text="Discount voucher:").grid(row=row, column=0, sticky="w")
        self.voucher_entry = ttk.Entry(main, textvariable=self.discount_code_var)
        self.voucher_entry.grid(row=row, column=1, sticky="ew")
        row += 1

        # Discount message (error/success) – empty at first
        self.discount_msg_label = ttk.Label(
            main, textvariable=self.discount_msg_var, foreground="blue"
        )
        self.discount_msg_label.grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1

        # Discount amount
        ttk.Label(main, text="Discount (RM):").grid(row=row, column=0, sticky="w")
        ttk.Label(main, textvariable=self.discount_var).grid(
            row=row, column=1, sticky="w"
        )
        row += 1

        # Tax amount
        ttk.Label(main, text="Tax (RM):").grid(row=row, column=0, sticky="w")
        ttk.Label(main, textvariable=self.tax_var).grid(
            row=row, column=1, sticky="w"
        )
        row += 1

        # Total
        ttk.Label(main, text="Total (RM):").grid(row=row, column=0, sticky="w")
        ttk.Label(main, textvariable=self.total_var).grid(
            row=row, column=1, sticky="w"
        )
        row += 1

        # Cash received
        ttk.Label(main, text="Cash received (RM):").grid(
            row=row, column=0, sticky="w"
        )
        self.cash_entry = ttk.Entry(main, textvariable=self.cash_received_var)
        self.cash_entry.grid(row=row, column=1, sticky="ew")
        row += 1

        # Balance
        ttk.Label(main, text="Balance (RM):").grid(row=row, column=0, sticky="w")
        ttk.Label(main, textvariable=self.balance_var).grid(
            row=row, column=1, sticky="w"
        )
        row += 1

        # Calculate button
        ttk.Button(
            main,
            text="Calculate",
            command=self.on_calculate,
        ).grid(row=row, column=0, columnspan=2, pady=(10, 0))
        row += 1

        # Checkout button
        ttk.Button(
            main,
            text="Checkout",
            command=self.on_checkout,
        ).grid(row=row, column=0, columnspan=2, pady=(5, 0))

    # -------- helpers / callbacks --------

    def _compute_subtotal(self) -> float:
        """Sum line_total from current_book_sale."""
        subtotal = 0.0
        for row in getattr(self.app, "current_book_sale", []) or []:
            # row: [book_id, sale_id, quantity, price_at_sale, line_total]
            try:
                subtotal += float(row[4])
            except (IndexError, ValueError, TypeError):
                continue
        return subtotal

    def on_calculate(self):
        # --- voucher / discount ---
        code = self.discount_code_var.get().strip().upper()
        vouchers = getattr(Sale_Service, "VOUCHERS", {})
        if code and code in vouchers:
            self.discount_rate = vouchers[code]
            percent = self.discount_rate * 100
            self.discount_msg_var.set(f"Voucher applied: {code} ({percent:.0f}% off)")
        elif code:
            self.discount_rate = 0.0
            self.discount_msg_var.set("Invalid voucher code")
        else:
            self.discount_rate = 0.0
            self.discount_msg_var.set("")  # no message if empty code

        # discount based on subtotal
        self.discount_value = self.subtotal_value * self.discount_rate
        if self.discount_value < 0:
            self.discount_value = 0.0

        discounted_subtotal = self.subtotal_value - self.discount_value
        if discounted_subtotal < 0:
            discounted_subtotal = 0.0

        # tax on discounted subtotal
        self.tax_value = discounted_subtotal * Sale_Service.TAX_RATE

        # total
        self.total_value = discounted_subtotal + self.tax_value

        # cash & balance
        cash_str = self.cash_received_var.get().strip()
        try:
            cash = float(cash_str) if cash_str else 0.0
        except ValueError:
            cash = 0.0
        self.balance_value = cash - self.total_value

        # update display vars
        self.discount_var.set(f"{self.discount_value:.2f}")
        self.tax_var.set(f"{self.tax_value:.2f}")
        self.total_var.set(f"{self.total_value:.2f}")
        self.balance_var.set(f"{self.balance_value:.2f}")

    def on_checkout(self):
        """
        Finalise the sale: push values into app.current_sale.
        No DB write yet, just store in-memory.
        """
        # Make sure everything is up to date even if user didn't press Calculate
        self.on_calculate()

        # Safely parse cash again (in case on_calculate didn't get called before)
        cash_str = self.cash_received_var.get().strip()
        try:
            cash = float(cash_str) if cash_str else 0.0
        except ValueError:
            cash = 0.0

        # Store sale summary on the app
        self.app.current_sale = {
            "sale_id": Uuid_Service.new_id(),
            "staff_id": getattr(self.app, "staff_id", None),
            "staff_name": getattr(self.app, "staff_name", None),
            "subtotal": self.subtotal_value,
            "discount_rate": self.discount_rate,
            "discount": self.discount_value,
            "tax": self.tax_value,
            "total": self.total_value,
            "cash_received": cash,
            "balance": self.balance_value,
            "voucher_code": self.discount_code_var.get().strip().upper(),
        }

        # NOTE: app.current_book_sale already contains the line items
        # We don't modify it here, just leave it as-is.

        Sale_Service.addSale(self.app.current_book_sale, self.app.current_sale)
        self.destroy()
