import uuid
from fastapi import HTTPException, status
from typing import List, Optional
from sqlmodel import Session, select, desc
from app.models.objeto import Objeto
from app.models.user import User
from app.schemas.objeto import ObjetoBase, ObjetoUpdate, ObjetoFinalizacao
from app.enums.objeto import StatusObjeto


class ObjetoService:
    def __init__(self, session: Session):
        self.session = session

    def fetch_objetos(
        self, 
        tipo: Optional[str] = None, 
        status: Optional[str] = None, 
        categoria: Optional[List[str]] = None,
        local_ocorrencia: Optional[List[str]] = None,
        search: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None
    ) -> List[Objeto]:
        query = select(Objeto).order_by(desc(Objeto.data_registro))
        if user_id:
            query = query.where(Objeto.user_id == user_id)
        if tipo:
            query = query.where(Objeto.tipo == tipo)
        if status:
            if status == "aberto":
                query = query.where((Objeto.status == "aberto") | (Objeto.status == "em_reivindicacao"))
            else:
                query = query.where(Objeto.status == status)
        if categoria:
            query = query.where(Objeto.categoria.in_(categoria))
        if local_ocorrencia:
            query = query.where(Objeto.local_ocorrencia.in_(local_ocorrencia))
        if search:
            search_term = f"%{search.lower()}%"
            query = query.where(
                (Objeto.nome.ilike(search_term)) |
                (Objeto.descricao.ilike(search_term)) |
                (Objeto.local_armazenamento.ilike(search_term)) |
                (Objeto.local_ocorrencia.ilike(search_term)) |
                (Objeto.local_especifico.ilike(search_term))
            )

        return self.session.exec(query).all()

    def get_objeto(self, objeto_id: uuid.UUID):
        objeto = self.session.get(Objeto, objeto_id)
        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objeto não encontrado")
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
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        
        objeto = self.session.get(Objeto, objeto_id)
        
        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objeto não encontrado")
        
        if objeto.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Objeto não pertence ao usuário")
        
        for key, value in objeto_data.model_dump(exclude_unset=True).items():
            setattr(objeto, key, value)
        objeto.motivo_finalizacao = None

        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)

        return objeto

    def finalizar_objeto(self, user_id: uuid.UUID, objeto_id: uuid.UUID, finalizacao_data: ObjetoFinalizacao) -> Objeto:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        
        objeto = self.session.get(Objeto, objeto_id)
        
        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objeto não encontrado")
        
        if objeto.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Objeto não pertence ao usuário")
        
        if objeto.status == StatusObjeto.finalizado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Objeto já foi finalizado")

        objeto.status = StatusObjeto.finalizado
        objeto.motivo_finalizacao = finalizacao_data.motivo_finalizacao

        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)

        return objeto

    def get_objetos_by_user_id(self, user_id: uuid.UUID) -> List[Objeto]:
        statement = select(Objeto).where(Objeto.user_id == user_id)
        objetos = self.session.exec(statement).all()
        return objetos