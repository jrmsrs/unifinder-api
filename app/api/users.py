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
from app.schemas.user import UserBase, UserRead

from app.services.objeto import get_objetos_by_user_id, create_objeto

router = APIRouter()

@router.get("/me")
def me(current_user: dict = Depends(get_user_session)):
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@router.get("/", response_model=Page[UserRead] )
def get_users(session: Session = Depends(get_session), current_user: dict = Depends(require_role("admin"))):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="User não encontrado")
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

@router.put("/")
def update_user():
    pass

@router.get("/{user_id}/objetos", response_model= Page[ObjetoRead])
def get_objetos(user_id: uuid.UUID, session: Session = Depends(get_session)):
    return paginate(get_objetos_by_user_id(session, user_id))

@router.post("/{user_id}/objetos", response_model=ObjetoRead)
def post_objeto(user_id: uuid.UUID, objeto_data: ObjetoBase, session: Session = Depends(get_session)):
    return create_objeto(session, user_id, objeto_data)