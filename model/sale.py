# model/sale.py

class Sale:
    SALE_FIELD = [
        "sale_id",
        "date_time",
        "staff_id",
        "subtotal",
        "tax",
        "discount",
        "total",
    ]
    SALE_HEADER = [
        "sale_id",
        "date_time",
        "staff_id",
        "subtotal",
        "tax",
        "discount",
        "total",
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