from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from schemas.objeto import ObjetoUpdate
from schemas.objeto import ObjetoBase
from models.objeto import Objeto
from schemas.objeto import ObjetoRead
from infra.database import get_session

router = APIRouter()

@router.get("/", response_model=List[ObjetoRead])
def get_objetos(session: Session = Depends(get_session)):
    objetos = session.exec(select(Objeto)).all()
    if not objetos:
        return Response(status_code=204)
    return objetos

@router.get("/{objeto_id}", response_model=ObjetoRead)
def get_objeto(objeto_id: int, session: Session = Depends(get_session)):
    obj = session.get(Objeto, objeto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")
    return obj

@router.post("/", response_model=ObjetoRead)
def create_objeto(objeto_in: ObjetoBase, session: Session = Depends(get_session)):
    obj = Objeto.model_validate(objeto_in)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.put("/{objeto_id}", response_model= ObjetoRead)
def update_objeto(objeto_id: int, objeto_in: ObjetoUpdate, session: Session = Depends(get_session)):
    obj = session.get(Objeto, objeto_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")

    obj_data = objeto_in.model_dump(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(obj, key, value)

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
