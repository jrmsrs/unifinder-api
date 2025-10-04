
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.enums.claim import StatusClaim

from app.models.claim import Claim
from app.schemas.claim import ClaimBase


def get_claim( session: Session, claim_id: uuid.UUID):
    query = select(Claim).where(Claim.id == claim_id)
    resultados = session.exec(query).all()
    return resultados

def update_claim( session: Session, claim_id: uuid.UUID, new_status: StatusClaim):
    claim = session.get(Claim, claim_id)

    if not claim:
        raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

    claim.status = new_status
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim

def create_claim(session: Session, claim_data: ClaimBase):
    claim = Claim (
        descricao=claim_data.descrição,
        local_ocorrencia=claim_data.local_ocorrencia,
        evidencias=claim_data.evidencias,
        objeto_id=claim_data.objeto_id,
        user_id=claim_data.user_id
    )
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim