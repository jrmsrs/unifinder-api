from typing import List
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.enums.claim import StatusClaim
from app.enums.objeto import StatusObjeto
from app.models.claim import Claim
from app.models.objeto import Objeto
from app.schemas.claim import ClaimBase, ClaimRead


def fetch_claims_by_objeto(session: Session, objeto_id: uuid.UUID) -> List[ClaimRead]:
    query = select(Claim).where(Claim.objeto_id == objeto_id)
    resultados = session.exec(query).all()
    return resultados

def fetch_claim( session: Session, claim_id: uuid.UUID):
    query = select(Claim).where(Claim.id == claim_id)
    claim = session.exec(query).first()
    return claim

def create_claim(session: Session, claim_data: ClaimBase, user_id: uuid.UUID):
    objeto = session.get(Objeto, claim_data.objeto_id)

    if objeto.status != StatusObjeto.aberto:
        raise HTTPException(status_code=400, detail="Objeto não disponível para reivindicação")

    claim = Claim (
        descricao=claim_data.descrição,
        local_ocorrencia=claim_data.local_ocorrencia,
        evidencias=claim_data.evidencias,
        objeto_id=claim_data.objeto_id,
        tutor_id=claim_data.tutor_id,
        user_id=user_id
    )
    session.add(claim)
    session.commit()
    session.refresh(claim)

    _update_status_objeto(session, claim_data.objeto_id, StatusObjeto.em_reinvidicação)

    return claim

def update_approve_claim( session: Session, user_id: uuid.UUID, claim_id: uuid.UUID):
    claim = session.get(Claim, claim_id)

    if not claim:
        raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

    if claim.tutor_id != user_id:
        raise HTTPException(status_code=403, detail="Usuário não autorizado a aprovar esta reivindicação")

    claim.status = StatusClaim.aprovada
    session.add(claim)
    session.commit()
    session.refresh(claim)

    _update_status_objeto(session, claim.objeto_id, StatusObjeto.aguardando_retirada)

    return claim

def update_reject_claim( session: Session, user_id: uuid.UUID, claim_id: uuid.UUID):
    claim = session.get(Claim, claim_id)

    if not claim:
        raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

    if claim.tutor_id != user_id:
        raise HTTPException(status_code=403, detail="Usuário não autorizado a rejeitar esta reivindicação")

    claim.status = StatusClaim.rejeitada
    session.add(claim)
    session.commit()
    session.refresh(claim)

    _update_status_objeto(session, claim.objeto_id, StatusObjeto.aberto)

    return claim

def update_finalize_claim(session: Session, user_id: uuid.UUID, claim_id: uuid.UUID):
    claim = session.get(Claim, claim_id)

    if not claim:
        raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

    if claim.user_id != user_id:
        raise HTTPException(status_code=403, detail="Usuário não autorizado a finalizar esta reivindicação")

    claim.status = StatusClaim.concluida
    session.add(claim)
    session.commit()
    session.refresh(claim)

    _update_status_objeto(session, claim.objeto_id, StatusClaim.concluida)

    return claim


def _update_status_objeto(session, objeto_id, new_status: StatusClaim):
    objeto = session.get(Objeto, objeto_id)

    objeto.status = new_status
    session.add(objeto)
    session.commit()
    session.refresh(objeto)
