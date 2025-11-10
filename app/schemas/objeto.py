from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime
from app.enums.objeto import TipoObjeto, StatusObjeto
from app.models.user import User

class ObjetoBase(BaseModel):
    nome: str
    descricao: str
    local_ocorrencia: str
    local_especifico: Optional[str] = None
    local_armazenamento: Optional[str] = None
    tipo: TipoObjeto
    url_imagem: Optional[str] = None
    categoria: str

class ObjetoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    local_ocorrencia: Optional[str] = None
    local_especifico: Optional[str] = None
    local_armazenamento: Optional[str] = None
    tipo: Optional[TipoObjeto] = None
    url_imagem: Optional[str] = None
    categoria: Optional[str] = None
    status: Optional[StatusObjeto] = None

class ObjetoFinalizacao(BaseModel):
    motivo_finalizacao: str

class ObjetoRead(ObjetoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    local_armazenamento: Optional[str] = None
    data_registro: datetime
    status: StatusObjeto
    motivo_finalizacao: Optional[str] = None
    user: User