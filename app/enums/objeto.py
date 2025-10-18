from enum import Enum

class TipoObjeto(str, Enum):
    achado = "ACHADO"
    perdido = "PERDIDO"

class StatusObjeto(str, Enum):
    aberto = "ABERTO"
    em_reinvidicação = "EM_REIVINDICACAO"
    aguardando_retirada = "AGUARDANDO_RETIRADA"
    finalizado = "FINALIZADO"