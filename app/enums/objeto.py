from enum import Enum

class TipoObjeto(str, Enum):
    achado = "ACHADO"
    perdido = "PERDIDO"

class StatusObjeto(str, Enum):
    aberto = "ABERTO"
    finalizado = "FINALIZADO"