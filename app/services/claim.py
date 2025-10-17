from typing import List, Optional
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.enums.claim import StatusClaim
from app.enums.objeto import StatusObjeto
from app.models.claim import Claim
from app.models.objeto import Objeto
from app.schemas.claim import ClaimBase, ClaimRead
from app.services.notify import NotificationService


class ClaimService:

    def __init__(self, session: Session, notification_service: NotificationService):
        self.session = session
        self.notifications = notification_service

    def fetch_claims_by_objeto(self, objeto_id: uuid.UUID) -> List[ClaimRead]:
        query = select(Claim).where(Claim.objeto_id == objeto_id)
        return self.session.exec(query).all()

    def fetch_claim(self, claim_id: uuid.UUID) -> Optional[Claim]:
        query = select(Claim).where(Claim.id == claim_id)
        return self.session.exec(query).first()

    def create_claim(self, claim_data: ClaimBase, user_id: uuid.UUID) -> Claim:
        objeto = self.session.get(Objeto, claim_data.objeto_id)

        if not objeto:
            raise HTTPException(status_code=404, detail="Objeto não encontrado")

        if objeto.status != StatusObjeto.aberto:
            raise HTTPException(status_code=400, detail="Objeto não disponível para reivindicação")

        claim = Claim(
            descricao=claim_data.descrição,
            local_ocorrencia=claim_data.local_ocorrencia,
            evidencias=claim_data.evidencias,
            objeto_id=claim_data.objeto_id,
            tutor_id=claim_data.tutor_id,
            user_id=user_id,
        )

        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim_data.objeto_id, StatusObjeto.em_reinvidicação)

        msg = f"O objeto {objeto.nome} tem uma nova reividicação!"

        self.notifications.notify_users(claim_data.tutor_id, msg)

        return claim


    def approve_claim(self, user_id: uuid.UUID, claim_id: uuid.UUID) -> Claim:
        claim = self.session.get(Claim, claim_id)

        if not claim:
            raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

        if claim.tutor_id != user_id:
            raise HTTPException(status_code=403, detail="Usuário não autorizado a aprovar esta reivindicação")

        claim.status = StatusClaim.aprovada
        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim.objeto_id, StatusObjeto.aguardando_retirada)

        msg = f"Sua reividicação para o id_objeto foi aprovada!"

        self.notifications.notify_users(claim.user_id, msg)

        return claim

    def reject_claim(self, user_id: uuid.UUID, claim_id: uuid.UUID) -> Claim:
        claim = self.session.get(Claim, claim_id)

        if not claim:
            raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

        if claim.tutor_id != user_id:
            raise HTTPException(status_code=403, detail="Usuário não autorizado a rejeitar esta reivindicação")

        claim.status = StatusClaim.rejeitada
        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim.objeto_id, StatusObjeto.aberto)

        msg = f"Sua reividicação para o id_objeto foi rejeitada!"

        self.notifications.notify_users(claim.user_id, msg)

        return claim

    def finalize_claim(self, user_id: uuid.UUID, claim_id: uuid.UUID) -> Claim:
        claim = self.session.get(Claim, claim_id)

        if not claim:
            raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

        if claim.user_id != user_id:
            raise HTTPException(status_code=403, detail="Usuário não autorizado a finalizar esta reivindicação")

        claim.status = StatusClaim.concluida
        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim.objeto_id, StatusObjeto.finalizado)

        return claim

    def _update_status_objeto(self, objeto_id: uuid.UUID, new_status: StatusObjeto):
        objeto = self.session.get(Objeto, objeto_id)
        if not objeto:
            raise HTTPException(status_code=404, detail="Objeto não encontrado")

        objeto.status = new_status
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
