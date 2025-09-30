from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime
from app.enums.objeto import TipoObjeto, StatusObjeto

class ObjetoBase(BaseModel):
    nome: str
    descricao: str
    local_ocorrencia: str
    tipo: TipoObjeto
    url_imagem: Optional[str] = None

class ObjetoUpdate(BaseModel):
    local_armazenamento: Optional[str] = None
    status: Optional[StatusObjeto] = None

class ObjetoRead(ObjetoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    local_armazenamento: Optional[str] = None
    data_registro: datetime
    status: StatusObjeto
