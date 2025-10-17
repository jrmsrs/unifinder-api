import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.auth import get_user_session
from app.infra.database import get_session
from app.integrations.sse_manager import SSEManager
from app.services.notify import NotificationService
from app.services.claim import ClaimService
from app.schemas.claim import ClaimBase, ClaimRead

router = APIRouter()



sse_manager = SSEManager()


# Dependency factory para NotificationService (injeção de dependência)
def get_notification_service(session: Session = Depends(get_session)) -> NotificationService:
    return NotificationService(sse_manager, session)


# Dependency factory para ClaimService
def get_claim_service(
    session: Session = Depends(get_session),
    notification_service: NotificationService = Depends(get_notification_service),
) -> ClaimService:
    return ClaimService(session, notification_service)



@router.get("/{claim_id}", response_model=ClaimRead)
def get_claim( claim_id: uuid.UUID, claim_service: ClaimService = Depends(get_claim_service)):
    return claim_service.fetch_claim(claim_id)


@router.post("/", response_model=ClaimRead)
def post_claim(
    claim_in: ClaimBase,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("id")
    return claim_service.create_claim(claim_in, user_id)


@router.put("/{claim_id}/aprovar", response_model=ClaimRead)
def approve_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("id")
    return claim_service.approve_claim(user_id, claim_id)


@router.put("/{claim_id}/rejeitar", response_model=ClaimRead)
def reject_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("id")
    return claim_service.reject_claim(user_id, claim_id)


@router.put("/{claim_id}/finalizar", response_model=ClaimRead)
def finalize_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("id")
    return claim_service.finalize_claim(user_id, claim_id)
