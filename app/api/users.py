from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from infra.database import get_session
from models.user import User
from schemas.user import UserBase

from schemas.user import UserRead

router = APIRouter()

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

