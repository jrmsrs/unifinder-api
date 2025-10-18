from typing import Optional
import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

class Notification(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivered: bool = False
