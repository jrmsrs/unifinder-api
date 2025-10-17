from typing import List

from sqlmodel import Session
from app.models.notify import Notification
from app.integrations.sse_manager import SSEManager

class NotificationService:
    def __init__(self, session: Session , sse_manager: SSEManager):
        self.sse = sse_manager
        self.session = session

    async def notify_users(self, user_ids: List[str], message: str):
        for user_id in user_ids:
            notify = await self._create_notification(user_id, message)
            await self.sse.send(user_id, notify.message)

    async def _create_notification(self, user_id: str, message: str) -> Notification:
        notify = Notification(user_id=user_id, message=message)
        self.session.add(notify)
        self.session.commit()
        self.session.refresh(notify)
        return notify

