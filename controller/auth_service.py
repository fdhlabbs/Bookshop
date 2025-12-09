# controller/auth_service.py
from model import Staff
import hashlib

class Auth_Service:
    @staticmethod
    def authenticate(username, password):
        username_exist = False
        password_correct = False

        # Always define these so they exist even on failure
        staff_id = None
        staff_name = None
        staff_role = None

        # Optional: early return if empty username/password
        if not username or not password:
            return username_exist, password_correct, staff_id, staff_name, staff_role

        staff = Staff()

        for row in staff.table:
            # row: [staff_id, name, username, password_hash, role]
            if row[2] == username:
                username_exist = True

                # store basic info even if password is wrong
                staff_id = row[0]
                staff_name = row[1]
                staff_role = row[4]

                if row[3] == Auth_Service.hash_password(password):
                    password_correct = True
                break

        return username_exist, password_correct, staff_id, staff_name, staff_role

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(input_password: str, stored_hash: str) -> bool:
        return Auth_Service.hash_password(input_password) == stored_hash
