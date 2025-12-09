# controller/debug.py

class Debug:
    @staticmethod
    def print(location, issue, no):
        print("========================================================")
        print("Location:" + location)
        print("Issue   :" + issue)
        print("No      :" + no)
        print("--------------------------------------------------------")