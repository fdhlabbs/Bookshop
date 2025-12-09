# model/__init__.py
from .book import Book
from .sale import Sale
from .staff import Staff
from .database import Database
from .book_sale import Book_Sale

__all__ = ["Book", "Sale", "Staff", "Database", "Book_Sale"]

print("model package initialized")
