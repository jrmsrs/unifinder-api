import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth.auth import get_user_session
from app.infra.database import get_session
from app.schemas.claim import ClaimBase, ClaimRead, ClaimUpdate
from app.services.claim import create_claim, fetch_claim, update_approve_claim, update_reject_claim, update_finalize_claim


router = APIRouter()

@router.get("/{claim_id}", response_model=ClaimRead)
def get_claim( claim_id: uuid.UUID, session: Session = Depends(get_session)):
    return fetch_claim(session, claim_id)

@router.post("/", response_model=ClaimRead)
def post_claim (claim_in: ClaimBase, session: Session = Depends(get_session), current_user: dict = Depends(get_user_session)):
    return create_claim(session, claim_in, current_user.get("id"))

@router.put("/{claim_id}/aprovar", response_model=ClaimRead)
def approve_claim(claim_id: uuid.UUID, session: Session = Depends(get_session), current_user: dict = Depends(get_user_session)):
    return update_approve_claim( session, claim_id, current_user.get("id"))

@router.put("/{claim_id}/reijeitar", response_model=ClaimRead)
def reject_claim(claim_id: uuid.UUID, session: Session = Depends(get_session), current_user: dict = Depends(get_user_session)):
    return update_reject_claim( session, claim_id, current_user.get("id"))

@router.put("/{claim_id}/finalizar", response_model=ClaimRead)
def finalize_claim(claim_id: uuid.UUID, session: Session = Depends(get_session), current_user: dict = Depends(get_user_session)):
    return update_finalize_claim( session, claim_id, current_user.get("id"))