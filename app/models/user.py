from typing import Optional, List, Dict, Any
import uuid
from sqlmodel import Field, Relationship, SQLModel, Column, JSON
from app.enums.user import TipoUser


class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    nome: str
    email: str
    username: str = Field(unique=True)
    role: TipoUser = Field(default=TipoUser.user)
    contato: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))

    objetos: List["Objeto"] = Relationship(back_populates="user")
    comentarios: List["Comentario"] = Relationship(back_populates="user")

