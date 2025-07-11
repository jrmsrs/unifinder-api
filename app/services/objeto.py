from fastapi import HTTPException, status
from sqlmodel import Session
from typing import List
from sqlmodel import Session, select
from models.objeto import Objeto
from models.user import User
from schemas.objeto import ObjetoBase

def get_objeto(session: Session, user_id: int, objeto_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    objeto = session.get(Objeto, objeto_id)
    return objeto

def create_objeto(session: Session, user_id: int, objeto_data: ObjetoBase) -> Objeto:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    objeto = Objeto(**objeto_data.model_dump(), user_id=user_id)
    session.add(objeto)
    session.commit()
    session.refresh(objeto)

    return objeto

def update_objeto(session: Session, user_id: int, objeto_id: int, objeto_data: ObjetoBase) -> Objeto:
    objeto = session.get(Objeto, objeto_id)
    
    if not objeto or objeto.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objeto não pertence ao usuário")

    objeto.local_armazenamento = objeto_data.local_armazenamento
    objeto.status = objeto_data.status

    session.add(objeto)
    session.commit()
    session.refresh(objeto)

    return objeto

def get_objetos_by_user_id(session: Session, user_id: int) -> List[Objeto]:
    statement = select(Objeto).where(Objeto.user_id == user_id)
    objetos = session.exec(statement).all()
    return objetos