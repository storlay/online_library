from enum import Enum


class UserRoleEnum(str, Enum):
    admin = "admin"
    author = "author"
    reader = "reader"
