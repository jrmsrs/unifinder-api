from typing import Optional
import uuid
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from app.auth.auth import get_user_session
from app.schemas.claim import ClaimRead
from app.schemas.comentario import ComentarioRead
from app.schemas.objeto import ObjetoBase, ObjetoUpdate, ObjetoRead, ObjetoFinalizacao
from app.services.claim import ClaimService
from app.services.comentario import ComentarioService
from app.services.factories import get_claim_service, get_objeto_service, get_comentario_service
from app.services.objeto import ObjetoService


router = APIRouter()


@router.post("/", response_model=ObjetoRead)
def post_objeto(
    objeto_data: ObjetoBase,
    objeto_service: ObjetoService = Depends(get_objeto_service),
    current_user: dict = Depends(get_user_session)
):
    user_id = current_user.get("user_id")
    return objeto_service.create_objeto(user_id, objeto_data)


@router.get("/", response_model=Page[ObjetoRead])
def get_objetos(
    tipo: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
    local_ocorrencia: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    user_id: Optional[uuid.UUID] = Query(default=None),
    objeto_service: ObjetoService = Depends(get_objeto_service)
):
    return paginate(objeto_service.fetch_objetos(tipo, status, categoria, local_ocorrencia, search, user_id))


@router.get("/{objeto_id}", response_model=ObjetoRead)
def get_objeto(
    objeto_id: uuid.UUID,
    objeto_service: ObjetoService = Depends(get_objeto_service)
):
    return objeto_service.get_objeto(objeto_id)


@router.put("/{objeto_id}", response_model=ObjetoRead)
def put_objeto(
    objeto_id: uuid.UUID,
    objeto_data: ObjetoUpdate,
    objeto_service: ObjetoService = Depends(get_objeto_service),
    current_user: dict = Depends(get_user_session)
):
    user_id = current_user.get("user_id")
    return objeto_service.update_objeto(user_id, objeto_id, objeto_data)


@router.put("/{objeto_id}/finalizar", response_model=ObjetoRead)
def finalizar_objeto(
    objeto_id: uuid.UUID,
    finalizacao_data: ObjetoFinalizacao,
    objeto_service: ObjetoService = Depends(get_objeto_service),
    current_user: dict = Depends(get_user_session)
):
    user_id = current_user.get("user_id")
    return objeto_service.finalizar_objeto(user_id, objeto_id, finalizacao_data)


@router.get("/{objeto_id}/comentarios", response_model=Page[ComentarioRead])
def get_comentarios(
    objeto_id: uuid.UUID,
    comentario_service: ComentarioService = Depends(get_comentario_service),
):
    return paginate(comentario_service.fetch_comentarios_by_objeto(objeto_id))


@router.get("/{objeto_id}/claims", response_model=Page[ClaimRead])
def get_claims(
    objeto_id: uuid.UUID,
    claim_service: ClaimService = Depends(get_claim_service)
):
    return paginate(claim_service.fetch_claims_by_objeto(objeto_id))