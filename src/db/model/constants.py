from enum import Enum

class UserRole(str, Enum):
    BASIC = "basic"
    ADMIN = "admin"
    FRIEND = "friend"

    @classmethod
    def list(cls):
        return [role.value for role in cls]
