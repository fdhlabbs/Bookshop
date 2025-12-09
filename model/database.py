# model/database.py
from pathlib import Path
import sys
import csv

class Database:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = super().__new__(cls)
        else:
            print("Using existing instance")

        return cls._instance




    def __init__(self):
        if self._initialized:
            return

        print("Initializing Database only once")

        self.set_dir()

        self.book = self.load_csv("book.csv")
        self.book_sale = self.load_csv("book_sale.csv")
        self.sale = self.load_csv("sale.csv")
        self.staff = self.load_csv("staff.csv")

        self._initialized = True
        return




    DIR = None
    def set_dir(self):
        if getattr(sys, 'frozen', False):
            self.DIR = Path(sys.executable).parent.parent
        else:
            self.DIR = Path(__file__).parent.parent






    def load_csv(self, csv_file):
        csv_path = self.DIR / "data" / csv_file

        if not csv_path.exists():
            return []

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            return rows
        








    def save_csv(self):
        data_dir = self.DIR / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        tables = {
            "book.csv": self.book,
            "book_sale.csv": self.book_sale,
            "sale.csv": self.sale,
            "staff.csv": self.staff,
        }

        for filename, rows in tables.items():
            csv_path = data_dir / filename
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows or []) 



        
#When you do varDB = Database(1,2,3), what actually returns?
#obj = Database.__new__(Database, 1, 2, 3)   # MUST return an object
#Database.__init__(obj, 1, 2, 3)             # return value is ignored
#varDB = obj
