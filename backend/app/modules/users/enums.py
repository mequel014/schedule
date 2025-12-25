# ./app/modules/users/enums.py

from enum import Enum


class UserRole(str, Enum):
    DOCTOR = "doctor"
    ADMIN = "admin"
    SYSADMIN = "sysadmin"