from enum import Enum

class Commands(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    LIST_MY_ACMD = "list:myacmd"
    LIST_ACMD = "list:acmd"
    LIST_MY_RSV = "list:myrsv"
    BOOK = "book"
    CANCEL = "cancel"