# model/book_sale.py

class Book_Sale:
    BOOK_SALE_FIELD = [
        "book_id",
        "sale_id",
        "quantity",
        "price_at_sale",
        "line_total",
    ]
    BOOK_SALE_HEADER = [
        "Book id",
        "Sale id",
        "Quantity",
        "Price at sale",
        "Line total",
    ]
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = super().__new__(cls)
        else:
            print("Using existing instance")

        return cls._instance






    def __init__(self, table = None):
        if self._initialized:
            return
        
        if table is None:
            raise ValueError("First time creation, must pass the table")


        print("Initializing table only once")
        self.table = table

        self._initialized = True