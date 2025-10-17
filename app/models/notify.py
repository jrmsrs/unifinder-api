from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime

from sqlmodel import Field

class Notification(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    sender_id: uuid.UUID = Field(foreign_key="user.id")
    receiver_id: uuid.UUID = Field(foreign_key="user.id")
    message: str
    created_at: datetime = datetime.utcnow()
    delivered: bool = False
