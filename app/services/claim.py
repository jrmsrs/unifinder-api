from typing import List, Optional
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.enums.claim import StatusClaim
from app.enums.objeto import StatusObjeto
from app.models.claim import Claim
from app.models.objeto import Objeto
from app.models.user import User
from app.schemas.claim import ClaimBase, ClaimRead, ClaimReview
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

    def fetch_claims_by_user(self, user_id: uuid.UUID) -> List[ClaimRead]:
        """Busca todas as claims feitas pelo usuário"""
        query = select(Claim).where(Claim.user_id == user_id)
        return self.session.exec(query).all()

    def fetch_pending_claims_by_tutor(self, tutor_id: uuid.UUID) -> List[ClaimRead]:
        """Busca claims atribuídas ao tutor que estão pendentes de aprovação"""
        query = select(Claim).where(
            Claim.tutor_id == tutor_id,
            Claim.status == StatusClaim.pendente
        )
        return self.session.exec(query).all()

    async def create_claim(self, claim_data: ClaimBase, user_id: uuid.UUID) -> Claim:
        objeto = self.session.get(Objeto, claim_data.objeto_id)

        if not objeto:
            raise HTTPException(status_code=404, detail="Objeto não encontrado")

        if objeto.status != StatusObjeto.aberto:
            raise HTTPException(status_code=400, detail="Objeto não disponível para reivindicação")

        claim = Claim(
            descricao=f"## Reivindicação ##\n\n{claim_data.descricao}",
            local_ocorrencia=claim_data.local_ocorrencia,
            evidencias=claim_data.evidencias,
            objeto_id=uuid.UUID(str(claim_data.objeto_id)),
            tutor_id=uuid.UUID(str(objeto.user_id)),
            user_id=uuid.UUID(str(user_id))
        )

        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim_data.objeto_id, StatusObjeto.em_reivindicacao)

        msg = f"O objeto {objeto.nome} tem uma nova reividicação!"

        self.notifications.notify_users([str(claim.tutor_id)], msg)

        return claim


    async def approve_claim(self, user_id: uuid.UUID, claim_id: uuid.UUID, claim_data: ClaimReview) -> Claim:
        claim = self.session.get(Claim, claim_id)

        if not claim:
            raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

        if str(claim.tutor_id) != user_id:

            raise HTTPException(status_code=403, detail="Usuário não autorizado a aprovar esta reivindicação")

        claim.status = StatusClaim.aprovada
        claim.descricao += f"\n\n[Réplica do Tutor]:\n\n{claim_data.motivo}"
        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim.objeto_id, StatusObjeto.aguardando_retirada)

        objeto = self.session.get(Objeto, claim.objeto_id)

        msg = f"Sua reividicação para o '{objeto.nome}' foi aprovada!"

        self.notifications.notify_users([str(claim.user_id)], msg)

        return claim

    async def reject_claim(self, user_id: uuid.UUID, claim_id: uuid.UUID, claim_data: ClaimReview) -> Claim:
        claim = self.session.get(Claim, claim_id)

        if not claim:
            raise HTTPException(status_code=404, detail="Reivindicação não encontrada")

        if str(claim.tutor_id) != user_id:
            raise HTTPException(status_code=403, detail="Usuário não autorizado a rejeitar esta reivindicação")

        claim.status = StatusClaim.rejeitada
        claim.descricao += f"\n\n[Réplica do Tutor]:\n\n{claim_data.motivo}"
        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        self._update_status_objeto(claim.objeto_id, StatusObjeto.aberto)

        objeto = self.session.get(Objeto, claim.objeto_id)
        msg = f"Sua reividicação para o '{objeto.nome}' foi rejeitada!"

        self.notifications.notify_users([str(claim.user_id)], msg)

        return claim

    async def finalize_claim(self, user_id: uuid.UUID, claim_id: uuid.UUID) -> Claim:
        claim = self.session.get(Claim, claim_id)

        if not claim:
            raise HTTPException(status_code=404, detail="Reivindicação não encontrada")
        if str(claim.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Usuário não autorizado a finalizar esta reivindicação")
            raise HTTPException(status_code=403, detail="Usuário não autorizado a finalizar esta reivindicação")

        claim.status = StatusClaim.concluida
        self.session.add(claim)
        self.session.commit()
        self.session.refresh(claim)

        user = self.session.get(User, claim.user_id)
        self._finalize_objeto(claim.objeto_id, f"Objeto entregue ao reivindicante {user.nome}")

        objeto = self.session.get(Objeto, claim.objeto_id)
        msg = f"Sua reividicação para o '{objeto.nome}' foi finalizada!"

        self.notifications.notify_users([str(claim.tutor_id)], msg)
        self.notifications.notify_users([str(claim.tutor_id)], msg)

        return claim

    def _update_status_objeto(self, objeto_id: uuid.UUID, new_status: StatusObjeto):
        objeto = self.session.get(Objeto, objeto_id)
        if not objeto:
            raise HTTPException(status_code=404, detail="Objeto não encontrado")

        objeto.status = new_status
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
    
    def _finalize_objeto(self, objeto_id: uuid.UUID, motivo_finalizacao: str):
        objeto = self.session.get(Objeto, objeto_id)
        if not objeto:
            raise HTTPException(status_code=404, detail="Objeto não encontrado")

        objeto.motivo_finalizacao = motivo_finalizacao
        objeto.status = StatusObjeto.finalizado
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
