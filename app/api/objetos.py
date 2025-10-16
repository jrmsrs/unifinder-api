from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate
from sqlmodel import Session
from app.schemas.claim import ClaimRead
from app.services.claim import fetch_claims_by_objeto
from app.services.comentario import fetch_comentarios_by_objeto
from app.schemas.comentario import ComentarioRead
from app.schemas.objeto import ObjetoUpdate
from app.schemas.objeto import ObjetoBase
from app.models.objeto import Objeto
from app.schemas.objeto import ObjetoRead
from app.infra.database import get_session
from app.services.objeto import fetch_objetos

router = APIRouter()

@router.get("/", response_model=Page[ObjetoRead])
def get_objetos(tipo: Optional[str] = Query(default=None), status: Optional[str] = Query(default=None), session: Session = Depends(get_session)):
    return paginate(fetch_objetos(session, tipo, status))

@router.get("/{objeto_id}", response_model=ObjetoRead)
def get_objeto(objeto_id: uuid.UUID, session: Session = Depends(get_session)):
    obj = session.get(Objeto, objeto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")
    return obj

@router.put("/{objeto_id}", response_model= ObjetoRead)
def put_objeto(objeto_id: uuid.UUID, objeto_in: ObjetoUpdate, session: Session = Depends(get_session)):
    obj = session.get(Objeto, objeto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")

    obj_data = objeto_in.model_dump(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(obj, key, value)

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/{objeto_id}/comentarios", response_model=Page[ComentarioRead])
def get_comentarios(objeto_id: uuid.UUID, session: Session = Depends(get_session)):
    return paginate(fetch_comentarios_by_objeto(session, objeto_id))


@router.get("/{objeto_id}/claims", response_model=Page[ClaimRead])
def get_claims(objeto_id: uuid.UUID, session: Session = Depends(get_session)):
    return paginate( fetch_claims_by_objeto(session, objeto_id))

