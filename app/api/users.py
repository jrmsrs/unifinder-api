from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from infra.database import get_session
from models.user import User
from schemas.user import UserBase, UserRead

from services.objeto import get_objetos_by_user_id, get_objeto

router = APIRouter()

@router.get("/", response_model=List[UserRead])
def get_user(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="User não encontrado")
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
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

@router.get("/{user_id}/objetos", response_model=List[UserRead])
def get_objetos_by_user(user_id: int, session: Session = Depends(get_session)):
    return get_objetos_by_user_id(session, user_id)
