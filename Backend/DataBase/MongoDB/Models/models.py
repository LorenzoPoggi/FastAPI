# models.py
# Archivo para definir los modelos de datos con Pydantic
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None # ID opcional para que el usuario no deba proporcionarlo y lo haga la db
    username: str
    email: str