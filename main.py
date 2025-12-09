# main.py
from controller import *
import tkinter as tk

def main():
    print("Main function running")

    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
