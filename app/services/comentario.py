
from typing import List
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from models.comentario import Comentario
from schemas.comentario import ComentarioBase, ComentarioRead, ComentarioUpdate


def fetch_comentarios_by_objeto(session: Session, objeto_id: uuid.UUID) -> List[ComentarioRead]:
    query = select(Comentario).where(Comentario.objeto_id == objeto_id)
    resultados = session.exec(query).all()
    return resultados
    
def create_comentario( session: Session, comentario_data: ComentarioBase) -> ComentarioRead:
    comentario = Comentario(
        conteudo=comentario_data.conteudo,
        objeto_id=comentario_data.objeto_id,
        user_id=comentario_data.user_id
    )
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario

def update_comentario( session: Session,  comentario_id: uuid.UUID, comentario_data: ComentarioUpdate) -> ComentarioRead:
    comentario = session.get(Comentario, comentario_id)

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    comentario.conteudo = comentario_data.conteudo
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario

def remove_comentario( session: Session, comentario_id: uuid.UUID):
    comentario = session.get(Comentario, comentario_id)

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    session.delete(comentario)
    session.commit()