from enum import Enum

class StatusClaim(str, Enum):
    pendente = "PENDENTE"
    aprovada = "APROVADA"
    rejeitada = "REJEITADA"