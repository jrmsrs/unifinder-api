
from fastapi import FastAPI
from sqlmodel import SQLModel
from api import objetos, users
from infra.database import engine

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(objetos.router, prefix='/objetos', tags=["Objetos"])
app.include_router(users.router, prefix='/users', tags=["Users"])