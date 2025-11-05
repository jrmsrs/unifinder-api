from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlmodel import Session, select
from app.auth.auth import get_user_session, require_role
from app.schemas.objeto import ObjetoRead
from app.schemas.objeto import ObjetoBase
from app.infra.database import get_session
from app.models.user import User
from app.schemas.user import UserBase, UserRead, UserUpdate
from app.services.objeto import ObjetoService
from app.services.factories import get_objeto_service

router = APIRouter()

@router.get("/me")
def me(current_user: dict = Depends(get_user_session)):
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@router.get("/", response_model=Page[UserRead] )
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return paginate(users)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User não encontrado")
    return user

@router.post("/", response_model=UserRead)
def create_user(user_in: UserBase, session: Session = Depends(get_session)):
    user = User.model_validate(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_user_session)
):
    """
    Atualiza dados do usuário.
    Apenas o próprio usuário pode atualizar seus dados.
    """
    # Verificar se o usuário está tentando atualizar seus próprios dados
    current_user_id = uuid.UUID(current_user.get("user_id"))
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Você só pode atualizar seus próprios dados")
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User não encontrado")
    
    # Atualizar apenas campos fornecidos
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.get("/{user_id}/objetos", response_model= Page[ObjetoRead])
def get_objetos(
    user_id: uuid.UUID, 
    objeto_service: ObjetoService = Depends(get_objeto_service)
):
    return paginate(objeto_service.get_objetos_by_user_id(user_id))

@router.post("/{user_id}/objetos", response_model=ObjetoRead)
def post_objeto(
    user_id: uuid.UUID, 
    objeto_data: ObjetoBase, 
    objeto_service: ObjetoService = Depends(get_objeto_service)
):
    return objeto_service.create_objeto(user_id, objeto_data)