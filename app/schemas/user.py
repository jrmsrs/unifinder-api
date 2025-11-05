
from typing import List, Optional, Dict, Any
import uuid
from pydantic import BaseModel
from app.models.objeto import Objeto
from app.enums.user import TipoUser

class UserBase(BaseModel):
    nome: str
    email: str
    username: str
    contato: Optional[List[Dict[str, Any]]] = None


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    username: Optional[str] = None
    contato: Optional[List[Dict[str, Any]]] = None


class UserRead(BaseModel):
    id: uuid.UUID
    nome: str
    username: str
    email: str
    role: TipoUser
    contato: Optional[List[Dict[str, Any]]] = None
    objetos: Optional[List[Objeto]] = []

    class Config:
        from_attributes = True