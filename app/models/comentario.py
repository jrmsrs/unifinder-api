import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import datetime

class Comentario(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conteudo: str
    publicado_em: datetime = Field(default_factory=datetime.utcnow)

    objeto_id: uuid.UUID = Field(foreign_key="objeto.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    username: str = Field(foreign_key="user.username")

    objeto: Optional["Objeto"] = Relationship(back_populates="comentarios")