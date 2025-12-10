# controller/sale_service.py
from model import Sale, Book_Sale, Book
from datetime import datetime
import copy


class Sale_Service:
    
    TAX_RATE = 0.06  # 6% GST/SST or similar
    
    VOUCHERS = {
        "": 0.00,
        "FIRSTTIMEBUY": 0.05,
        "RAYA": 0.07,
    }

    @staticmethod
    def get_book_for_display(current_book_sale):
        """
        Returns a list of books (deep copy of Book.table) with stock reduced
        according to current_book_sale, and any books with stock <= 0 removed.

        Assumptions:
        - Book().table is a list of rows with NO header.
        - Each row in book.table is:
          [book_id, title, author, category, isbn, price, stock]
        - current_book_sale is ALREADY AGGREGATED:
          no two rows have the same book_id.
        - Each row in current_book_sale is:
          [book_id, sale_id, quantity, price_at_sale, line_total]
        """

        book = Book()  # singleton instance, already initialized in App

        # if book.table empty return empty table
        if not book.table:
            return []

        # Work on a deep copy so we don't mutate the main table
        book_for_display = copy.deepcopy(book.table)

        # For each sale line, adjust stock in book_for_display
        for row_book_sale in current_book_sale:
            book_id = row_book_sale[0]
            qty_str = row_book_sale[2]

            try:
                qty = int(qty_str)
            except (TypeError, ValueError):
                qty = 0  # bad data? treat as 0

            # Find the matching book row in book_for_display
            for i, row_book in enumerate(book_for_display):
                # Book row: [book_id, title, author, category, isbn, price, stock]
                if row_book[0] == book_id:
                    stock_str = row_book[6]

                    try:
                        stock = int(stock_str)
                    except (TypeError, ValueError):
                        stock = 0

                    stock -= qty

                    if stock <= 0:
                        # Remove the book entirely if out of stock or negative
                        del book_for_display[i]
                    else:
                        # Update stock (as string, to be consistent with CSV data)
                        row_book[6] = str(stock)

                    # Important: break because book_id is unique in current_book_sale
                    break

        return book_for_display














    @staticmethod
    def aggregate_book_same_id(current_book_sale):
        """
        current_book_sale rows:
        [book_id, sale_id, quantity, price_at_sale, line_total]
        """
        aggregated = {}

        for row in current_book_sale:
            book_id = row[0]
            sale_id = row[1]

            try:
                qty = int(row[2])
            except (TypeError, ValueError):
                qty = 0

            try:
                price = float(row[3])
            except (TypeError, ValueError):
                price = 0.0

            if book_id not in aggregated:
                aggregated[book_id] = [
                    book_id,
                    sale_id,
                    qty,
                    row[3],                # price_at_sale as string
                    f"{qty * price:.2f}",  # line_total
                ]
            else:
                aggregated[book_id][2] += qty
                total_qty = aggregated[book_id][2]
                aggregated[book_id][4] = f"{total_qty * price:.2f}"

        return list(aggregated.values())












    @staticmethod
    def add_book_to_current_book_sale(current_book_sale, book_row, quantity, sale_id):
        """
        Add `quantity` units of `book_row` into current_book_sale,
        then aggregate so there is at most one row per book_id.

        book_row from Book table:
            [book_id, title, author, category, isbn, price, stock]

        Returns a NEW list of book_sale rows:
            [book_id, sale_id, quantity, price_at_sale, line_total]
        """
        if current_book_sale is None:
            current_book_sale = []

        book_id = book_row[0]
        price_str = book_row[5]  # Book.price (string)

        try:
            qty = int(quantity)
        except (TypeError, ValueError):
            qty = 0

        try:
            price = float(price_str)
        except (TypeError, ValueError):
            price = 0.0

        line_total = f"{qty * price:.2f}"

        new_row = [
            book_id,
            sale_id,
            str(qty),
            price_str,
            line_total,
        ]

        updated = list(current_book_sale)
        updated.append(new_row)

        # Aggregate by book_id
        aggregated = Sale_Service.aggregate_book_same_id(updated)

        # Ensure all rows use the provided sale_id in column 1
        for row in aggregated:
            row[1] = sale_id

        return aggregated
    







    @staticmethod
    def addSale(book_sale, sale):
        """
        book_sale  -> app.current_book_sale (list of line items)
        sale       -> app.current_sale (dictionary)
        """

        if not book_sale or not sale:
            return  # nothing to save

        sale_table = Sale().table
        book_sale_table = Book_Sale().table
        book_table = Book().table

        sale_id = sale.get("sale_id")

        # --------- 1. ADD SALE RECORD ----------
        sale_row = [
            sale_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sale.get("staff_id"),
            f"{sale.get('subtotal', 0):.2f}",
            f"{sale.get('tax', 0):.2f}",
            f"{sale.get('discount', 0):.2f}",
            f"{sale.get('total', 0):.2f}",
        ]
        sale_table.append(sale_row)

        # --------- 2. UPDATE BOOK STOCK ----------
        for bs_row in book_sale:
            # bs_row: [book_id, sale_id, quantity, price_at_sale, line_total]
            book_id = bs_row[0]
            qty_str = bs_row[2]

            try:
                qty = int(qty_str)
            except (TypeError, ValueError):
                qty = 0

            if qty <= 0:
                continue

            # find matching book in Book.table
            for book_row in book_table:
                # book_row: [book_id, title, author, category, isbn, price, stock]
                if book_row[0] == book_id:
                    try:
                        stock = int(book_row[6])
                    except (TypeError, ValueError):
                        stock = 0

                    new_stock = stock - qty
                    if new_stock < 0:
                        new_stock = 0

                    book_row[6] = str(new_stock)
                    break  # stop after matching book_id

        # --------- 3. ADD BOOK_SALE RECORDS ----------
        # Force all line items to use the final sale_id
        for row in book_sale:
            row[1] = sale_id  # overwrite placeholder / old id
            book_sale_table.append(row)

        print("Sale saved successfully.")