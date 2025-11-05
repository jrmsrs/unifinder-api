"""
Factory functions para injeção de dependência dos serviços
"""
from fastapi import Depends
from sqlmodel import Session
from app.infra.database import get_session
from app.services.comentario import ComentarioService
from app.services.objeto import ObjetoService
from app.services.notify import NotificationService
from app.services.claim import ClaimService


def get_comentario_service(session: Session = Depends(get_session)) -> ComentarioService:
    return ComentarioService(session)


def get_objeto_service(session: Session = Depends(get_session)) -> ObjetoService:
    return ObjetoService(session)


def get_notification_service(
    session: Session = Depends(get_session)
) -> NotificationService:
    return NotificationService(session)


def get_claim_service(
    session: Session = Depends(get_session),
    notification_service: NotificationService = Depends(get_notification_service),
) -> ClaimService:
    return ClaimService(session, notification_service)
