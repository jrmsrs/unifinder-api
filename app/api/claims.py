import uuid
from fastapi import APIRouter, Depends

from app.auth.auth import get_user_session
from app.services.claim import ClaimService
from app.services.factories import get_claim_service
from app.schemas.claim import ClaimBase, ClaimRead

router = APIRouter()



@router.get("/{claim_id}", response_model=ClaimRead)
def get_claim( claim_id: uuid.UUID, claim_service: ClaimService = Depends(get_claim_service)):
    return claim_service.fetch_claim(claim_id)


@router.post("/", response_model=ClaimRead)
async def post_claim(
    claim_in: ClaimBase,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.create_claim(claim_in, user_id)


@router.put("/{claim_id}/aprovar", response_model=ClaimRead)
async def approve_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.approve_claim(user_id, claim_id)


@router.put("/{claim_id}/rejeitar", response_model=ClaimRead)
async def reject_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.reject_claim(user_id, claim_id)


@router.put("/{claim_id}/finalizar", response_model=ClaimRead)
async def finalize_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.finalize_claim( user_id, claim_id)
