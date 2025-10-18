
from typing import List
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.comentario import Comentario
from app.schemas.comentario import ComentarioBase, ComentarioRead, ComentarioUpdate


class ComentarioService:
    def __init__(self, session: Session):
        self.session = session

    def fetch_comentarios_by_objeto(self, objeto_id: uuid.UUID) -> List[ComentarioRead]:
        query = select(Comentario).where(Comentario.objeto_id == objeto_id)
        resultados = self.session.exec(query).all()
        return resultados
        
    def create_comentario(self, comentario_data: ComentarioBase) -> ComentarioRead:
        comentario = Comentario(
            conteudo=comentario_data.conteudo,
            objeto_id=comentario_data.objeto_id,
            user_id=comentario_data.user_id,
            username=comentario_data.username
        )
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    def update_comentario(self, comentario_id: uuid.UUID, comentario_data: ComentarioUpdate) -> ComentarioRead:
        comentario = self.session.get(Comentario, comentario_id)

        if not comentario:
            raise HTTPException(status_code=404, detail="Comentário não encontrado")

        comentario.conteudo = comentario_data.conteudo
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    def remove_comentario(self, comentario_id: uuid.UUID):
        comentario = self.session.get(Comentario, comentario_id)

        if not comentario:
            raise HTTPException(status_code=404, detail="Comentário não encontrado")

        self.session.delete(comentario)
        self.session.commit()