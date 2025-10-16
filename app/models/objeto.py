import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime

from app.models.user import User
from app.enums.objeto import TipoObjeto, StatusObjeto


class Objeto(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    nome: str
    descricao: str
    local_ocorrencia: str
    local_armazenamento: str = Field(default=None, nullable=True)
    tipo: TipoObjeto
    status: StatusObjeto = Field(default=StatusObjeto.aberto)
    data_registro: datetime = Field(default_factory=datetime.utcnow)
    url_imagem: str = Field(default=None, nullable=True)
    categoria: str

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="objetos")

    comentarios: List["Comentario"] = Relationship(back_populates="objeto")