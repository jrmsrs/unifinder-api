
from typing import List, Optional
import uuid
from pydantic import BaseModel
from app.models.objeto import Objeto
from app.enums.user import TipoUser

class UserBase(BaseModel):
    nome: str
    email: str
    username: str


class UserRead(BaseModel):
    id: uuid.UUID
    nome: str
    username: str
    email: str
    role: TipoUser
    objetos: Optional[List[Objeto]] = []