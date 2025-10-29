import uuid
from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional, List
from datetime import datetime
from app.enums.claim import StatusClaim

class Claim(SQLModel, table=True):

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    descricao: Optional[str] = None
    local_ocorrencia: Optional[str] = None
    data_ocorrencia: Optional[str] = None
    evidencias: Optional[List[str]] = Field(sa_column=Column(JSON))

    status: StatusClaim = Field(default=StatusClaim.pendente)
    data_registro: datetime = Field(default_factory=datetime.utcnow)

    objeto_id: uuid.UUID = Field(foreign_key="objeto.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    tutor_id: uuid.UUID = Field(foreign_key="user.id")