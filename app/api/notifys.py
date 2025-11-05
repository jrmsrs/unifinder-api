from typing import List
import uuid
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from app.auth.auth import get_user_session
from app.services.notify import NotificationService
from app.services.factories import get_notification_service
from app.schemas.notify import NotificationRead

router = APIRouter()


@router.get("/", response_model=Page[NotificationRead])
def get_notifications(
    unread_only: bool = Query(default=False, description="Retornar apenas não lidas"),
    current_user: dict = Depends(get_user_session),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """
    Busca notificações do usuário autenticado.
    """
    user_id = uuid.UUID(current_user.get("user_id"))
    notifications = notification_service.get_user_notifications(user_id, unread_only=unread_only)
    return paginate(notifications)



@router.put("/{notification_id}/mark-as-read", response_model=NotificationRead)
def mark_notification_as_read(
    notification_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """
    Marca uma notificação específica como lida.
    """
    from fastapi import HTTPException, status
    
    user_id = uuid.UUID(current_user.get("user_id"))
    try:
        notification = notification_service.mark_as_delivered(notification_id, user_id)
        return notification
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/mark-all-as-read")
def mark_all_as_read(
    current_user: dict = Depends(get_user_session),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """
    Marca todas as notificações do usuário autenticado como lidas.
    """
    user_id = uuid.UUID(current_user.get("user_id"))
    count = notification_service.mark_all_as_delivered(user_id)
    return {"marked": count, "message": f"{count} notificações marcadas como lidas"}
