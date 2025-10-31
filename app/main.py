
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlmodel import SQLModel
from app.api import objetos, users, comentarios, claims, notifys
from app.infra.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="UnifinderAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SQLModel.metadata.create_all(engine)

app.include_router(objetos.router, prefix='/objetos', tags=["Objetos"])
app.include_router(users.router, prefix='/users', tags=["Users"])
app.include_router(comentarios.router, prefix='/comentarios', tags=["Comentarios"])
app.include_router(claims.router, prefix='/claims', tags=["Claims"])
app.include_router(notifys.router, prefix='/notifys', tags=["Notifys"])

add_pagination(app)