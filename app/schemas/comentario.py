from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ComentarioBase(BaseModel):
    conteudo: str = Field(..., min_length=1)
    objeto_id: int
    user_id: int

class ComentarioUpdate(BaseModel):
    conteudo: str = Field(..., min_length=1)

class ComentarioRead(ComentarioBase):
    id: int
    publicado_em: datetime
    objeto_id: int
    user_id: int
