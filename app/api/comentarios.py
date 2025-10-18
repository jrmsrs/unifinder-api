import uuid
from fastapi import APIRouter, Depends
from app.schemas.comentario import ComentarioBase, ComentarioUpdate, ComentarioRead
from app.services.comentario import ComentarioService
from app.services.factories import get_comentario_service

router = APIRouter()


@router.post("/", response_model=ComentarioRead)
def post_comentario(
    comentario: ComentarioBase, 
    comentario_service: ComentarioService = Depends(get_comentario_service)
):
    return comentario_service.create_comentario(comentario)

@router.put("/{comentario_id}", response_model=ComentarioRead)
def put_comentario(
    comentario_id: uuid.UUID, 
    comentario: ComentarioUpdate, 
    comentario_service: ComentarioService = Depends(get_comentario_service)
):
    return comentario_service.update_comentario(comentario_id, comentario)

@router.delete("/{comentario_id}")
def delete_comentario(
    comentario_id: uuid.UUID,
    comentario_service: ComentarioService = Depends(get_comentario_service)
):
    comentario_service.remove_comentario(comentario_id)
    return {"message": "Comentário removido com sucesso"}