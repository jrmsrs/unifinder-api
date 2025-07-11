from enum import Enum

class TipoUser(str, Enum):
    admin = "ADMIN"
    user = "USER"
    funcionario = "FUNCIONARIO"