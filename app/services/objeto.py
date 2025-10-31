import uuid
from fastapi import HTTPException, status
from typing import List, Optional
from sqlmodel import Session, select, desc
from app.models.objeto import Objeto
from app.models.user import User
from app.schemas.objeto import ObjetoBase, ObjetoUpdate


class ObjetoService:
    def __init__(self, session: Session):
        self.session = session

    def fetch_objetos(self, tipo: Optional[str] = None, status: Optional[str] = None, categoria: Optional[str] = None, local_ocorrencia: Optional[str] = None, search: Optional[str] = None) -> List[Objeto]:
        query = select(Objeto).order_by(desc(Objeto.data_registro))

        if tipo:
            query = query.where(Objeto.tipo == tipo)
        if status:
            if status == "aberto":
                query = query.where((Objeto.status == "aberto") | (Objeto.status == "em_reivindicacao"))
            else:
                query = query.where(Objeto.status == status)
        if categoria:
            query = query.where(Objeto.categoria == categoria)
        if local_ocorrencia:
            query = query.where(Objeto.local_ocorrencia == local_ocorrencia)
        if search:
            search_term = f"%{search.lower()}%"
            query = query.where(
                (Objeto.nome.ilike(search_term)) |
                (Objeto.descricao.ilike(search_term)) |
                (Objeto.local_armazenamento.ilike(search_term))
            )

        return self.session.exec(query).all()

    def get_objeto(self, objeto_id: uuid.UUID):
        objeto = self.session.get(Objeto, objeto_id)
        if not objeto:
            raise HTTPException(status_code=404, detail="Objeto não encontrado")
        return objeto

    def create_objeto(self, user_id: uuid.UUID, objeto_data: ObjetoBase) -> Objeto:
        user = self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        objeto = Objeto(**objeto_data.model_dump(), user_id=user_id)
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)

        return objeto

    def update_objeto(self, user_id: uuid.UUID, objeto_id: uuid.UUID, objeto_data: ObjetoUpdate) -> Objeto:
        objeto = self.session.get(Objeto, objeto_id)
        
        if not objeto or objeto.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objeto não pertence ao usuário")

        objeto.local_armazenamento = objeto_data.local_armazenamento
        objeto.status = objeto_data.status

        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)

        return objeto

    def get_objetos_by_user_id(self, user_id: uuid.UUID) -> List[Objeto]:
        statement = select(Objeto).where(Objeto.user_id == user_id)
        objetos = self.session.exec(statement).all()
        return objetos