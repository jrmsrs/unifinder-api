
from pydantic import BaseModel


class UserBase(BaseModel):
    nome: str
    email: str
    senha: str

class UserRead(BaseModel):
    nome: str
    email: str