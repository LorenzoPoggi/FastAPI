# models.py
# Archivo para definir los modelos de datos con Pydantic
from pydantic import BaseModel

class User(BaseModel):
    id: str | None # ID opcional para que el usuario no deba proporcionarlo y lo haga la db
    username: str
    email: str