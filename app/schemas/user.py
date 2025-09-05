
from typing import List, Optional
import uuid
from pydantic import BaseModel
from models.objeto import Objeto
from enums.user import TipoUser

class UserBase(BaseModel):
    nome: str
    email: str
    senha: str


class UserRead(BaseModel):
    id: uuid.UUID
    nome: str
    email: str
    role: TipoUser
    objetos: Optional[List[Objeto]] = []