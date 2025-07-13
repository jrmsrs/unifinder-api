from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import datetime

class Comentario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conteudo: str
    publicado_em: datetime = Field(default_factory=datetime.utcnow)

    objeto_id: int = Field(foreign_key="objeto.id")
    user_id: int = Field(foreign_key="user.id")

    objeto: Optional["Objeto"] = Relationship(back_populates="comentarios")