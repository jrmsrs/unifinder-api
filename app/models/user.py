from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from enums.user import TipoUser


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    role: TipoUser = Field(default=TipoUser.user)

    objetos: List["Objeto"] = Relationship(back_populates="user")

