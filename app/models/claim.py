import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from app.enums.claim import StatusClaim

class Claim(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    descricao: str
    local_ocorrencia: str
    data_acorrencia: str
    status: StatusClaim = Field(default=StatusClaim.pendente)
    data_registro: datetime = Field(default_factory=datetime.utcnow)

    objeto_id: uuid.UUID = Field(foreign_key="objeto.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")