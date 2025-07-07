from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from enums.objeto import TipoObjeto, StatusObjeto


class Objeto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    local_ocorrencia: str
    local_armazenamento: str = Field(default=None, nullable=True)
    tipo: TipoObjeto
    status: StatusObjeto = Field(default=StatusObjeto.aberto)
    data_registro: datetime = Field(default_factory=datetime.utcnow)