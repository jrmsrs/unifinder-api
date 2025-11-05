from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime


class NotificationBase(BaseModel):
    message: str


class NotificationRead(NotificationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    delivered: bool

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    delivered: Optional[bool] = None
