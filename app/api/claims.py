import uuid
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate

from app.auth.auth import get_user_session
from app.services.claim import ClaimService
from app.services.factories import get_claim_service
from app.schemas.claim import ClaimBase, ClaimRead, ClaimReview

router = APIRouter()


@router.get("/me", response_model=Page[ClaimRead])
def get_my_claims(
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service)
):
    """Busca todas as claims feitas pelo usuário autenticado"""
    user_id = current_user.get("user_id")
    return paginate(claim_service.fetch_claims_by_user(user_id))


@router.get("/pending", response_model=Page[ClaimRead])
def get_pending_claims(
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service)
):
    """Busca claims atribuídas ao usuário autenticado que estão pendentes de aprovação"""
    user_id = current_user.get("user_id")
    return paginate(claim_service.fetch_pending_claims_by_tutor(user_id))


@router.get("/{claim_id}", response_model=ClaimRead)
def get_claim(claim_id: uuid.UUID, claim_service: ClaimService = Depends(get_claim_service)):
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
    claim_data: ClaimReview,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.approve_claim(user_id, claim_id, claim_data)


@router.put("/{claim_id}/rejeitar", response_model=ClaimRead)
async def reject_claim(
    claim_id: uuid.UUID,
    claim_data: ClaimReview,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.reject_claim(user_id, claim_id, claim_data)


@router.put("/{claim_id}/finalizar", response_model=ClaimRead)
async def finalize_claim(
    claim_id: uuid.UUID,
    current_user: dict = Depends(get_user_session),
    claim_service: ClaimService = Depends(get_claim_service),
):
    user_id = current_user.get("user_id")
    return await claim_service.finalize_claim( user_id, claim_id)
