import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user import UserRead

class ComentarioBase(BaseModel):
    conteudo: str = Field(..., min_length=1)
    objeto_id: uuid.UUID
    user_id: uuid.UUID
    username: str

class ComentarioUpdate(BaseModel):
    conteudo: str = Field(..., min_length=1)

class ComentarioRead(ComentarioBase):
    id: uuid.UUID
    publicado_em: datetime
    objeto_id: uuid.UUID
    user_id: uuid.UUID
    user: Optional[UserRead] = None

    class Config:
        from_attributes = True
