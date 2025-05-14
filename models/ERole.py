from enum import Enum

class ERole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_MODERATOR = "ROLE_MODERATOR"
    ROLE_ADMIN = "ROLE_ADMIN"
