from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from enums.claim import StatusClaim

class Claim(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    local_ocorrencia: str
    data_acorrencia: str
    status: StatusClaim = Field(default=StatusClaim.pendente)
    data_registro: datetime = Field(default_factory=datetime.utcnow)

    objeto_id: int = Field(foreign_key="objeto.id")
    user_id: int = Field(foreign_key="user.id")