from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime
from enums.objeto import TipoObjeto, StatusObjeto

class ObjetoBase(BaseModel):
    nome: str
    descricao: str
    local_ocorrencia: str
    tipo: TipoObjeto

class ObjetoUpdate(BaseModel):
    local_armazenamento: Optional[str] = None
    status: Optional[StatusObjeto] = None

class ObjetoRead(ObjetoBase):
    id: uuid.UUID
    local_armazenamento: Optional[str] = None
    data_registro: datetime
    status: StatusObjeto
