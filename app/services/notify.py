from typing import List
import uuid
import logging
from sqlmodel import Session, select
from app.models.notify import Notification
from app.schemas.notify import NotificationRead

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, session: Session):
        self.session = session

    def notify_users(self, user_ids: List[str], message: str):
        """
        Cria notificações no banco de dados para os usuários especificados.
        """
        notifications_created = []
        for user_id in user_ids:
            try:
                notify = self._create_notification(user_id, message)
                notifications_created.append(notify)
            except Exception as e:
                logger.error(f"Erro ao criar notificação para usuário {user_id}: {e}")
                self.session.rollback()
                # Continuar com outros usuários mesmo se um falhar
        
        return notifications_created

    def _create_notification(self, user_id: str, message: str) -> Notification:
        """Cria notificação no banco de dados"""
        try:
            notify = Notification(
                user_id=uuid.UUID(user_id),
                message=message,
                delivered=False
            )
            self.session.add(notify)
            self.session.commit()
            self.session.refresh(notify)
            return notify
        except Exception as e:
            logger.error(f"Erro ao criar notificação para {user_id}: {e}")
            self.session.rollback()
            raise

    def get_user_notifications(self, user_id: uuid.UUID, unread_only: bool = False) -> List[NotificationRead]:
        """Busca notificações do usuário"""
        query = select(Notification).where(Notification.user_id == user_id)
        
        if unread_only:
            query = query.where(Notification.delivered == False)
        
        query = query.order_by(Notification.created_at.desc())
        
        notifications = self.session.exec(query).all()
        return notifications

    def mark_as_delivered(self, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        """Marca notificação como entregue/lida"""
        notification = self.session.get(Notification, notification_id)
        
        if not notification:
            raise ValueError("Notificação não encontrada")
        
        if notification.user_id != user_id:
            raise ValueError("Notificação não pertence ao usuário")
        
        notification.delivered = True
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        
        return notification

    def mark_all_as_delivered(self, user_id: uuid.UUID) -> int:
        """Marca todas as notificações do usuário como entregues"""
        notifications = self.session.exec(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.delivered == False
            )
        ).all()
        
        count = 0
        for notification in notifications:
            notification.delivered = True
            self.session.add(notification)
            count += 1
        
        self.session.commit()
        return count

    def get_unread_count(self, user_id: uuid.UUID) -> int:
        """Retorna contagem de notificações não lidas"""
        notifications = self.session.exec(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.delivered == False
            )
        ).all()
        return len(notifications)

