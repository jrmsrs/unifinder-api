
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlmodel import SQLModel
from app.api import objetos, users, comentarios, claims
from app.infra.database import engine

app = FastAPI()

# SQLModel.metadata.create_all(engine)

app.include_router(objetos.router, prefix='/objetos', tags=["Objetos"])
app.include_router(users.router, prefix='/users', tags=["Users"])
app.include_router(comentarios.router, prefix='/comentarios', tags=["Comentarios"])
app.include_router(claims.router, prefix='/claims', tags=["Claims"])

add_pagination(app)