# model/book.py

class Book:
    BOOK_FIELD = [
        "book_id",
        "title",
        "author",
        "category",
        "isbn",
        "price",
        "stock",
    ]
    BOOK_HEADER = [
        "Book id",
        "Title",
        "Author",
        "Category",
        "Isbn",
        "Price",
        "Stock",
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