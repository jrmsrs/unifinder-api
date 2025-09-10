import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.comentario import ComentarioBase, ComentarioUpdate, ComentarioRead
from app.services.comentario import create_comentario, update_comentario, remove_comentario
from app.infra.database import get_session


router = APIRouter()


@router.post("/", response_model=ComentarioRead)
def post_comentario( comentario: ComentarioBase, session: Session = Depends(get_session)):
    return create_comentario(session, comentario )

@router.put("/{comentario_id}", response_model=ComentarioRead)
def put_comentario(comentario_id: uuid.UUID, comentario: ComentarioUpdate, session: Session = Depends(get_session)):
    return update_comentario(session, comentario_id, comentario)

@router.delete("/{comentario_id}")
def delete_comentario(comentario_id: uuid.UUID, session: Session = Depends(get_session)):
    return remove_comentario(session, comentario_id)