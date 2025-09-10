from typing import Optional, List
import uuid
from sqlmodel import Field, Relationship, SQLModel
from app.enums.user import TipoUser


class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    nome: str
    email: str
    username: str
    role: TipoUser = Field(default=TipoUser.user)

    objetos: List["Objeto"] = Relationship(back_populates="user")

