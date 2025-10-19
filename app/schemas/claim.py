import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.enums.claim import StatusClaim

class ClaimBase(BaseModel):
    descrição: Optional[str] = None
    local_ocorrencia: Optional[str] = None
    data_ocorrencia: Optional[str] = None
    evidencias: Optional[List[str]] = Field(default_factory=list)
    objeto_id: uuid.UUID

class ClaimRead(ClaimBase):
    id: uuid.UUID
    data_registro: datetime
    status: StatusClaim
    objeto_id: uuid.UUID
    user_id: uuid.UUID
    tutor_id: uuid.UUID