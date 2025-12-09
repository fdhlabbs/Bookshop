# controller/uuid_service.py
import uuid

class Uuid_Service:
    @staticmethod
    def new_id() -> str:
        return uuid.uuid4().hex

