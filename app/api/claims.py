from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi_pagination import Page, paginate
from sqlmodel import Session
from app.infra.database import get_session


router = APIRouter()

@router.get("/{claim_id}", response_model=Page[])
def get_claim(objeto_id: uuid.UUID, claim_id: uuid.UUID, session: Session = Depends(get_session)):
    pass

@router.post("/", response_model=Page[])
def create_claim(objeto_id: uuid.UUID, session: Session = Depends(get_session)):
    pass

@router.put("/{claim_id}", response_model=Page[])
def update_claim(objeto_id: uuid.UUID, claim_id: uuid.UUID, session: Session = Depends(get_session)):
    pass