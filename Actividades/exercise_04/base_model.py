# base_model.py - Sistema de Gestión de inventario
# Base de Datos simulada

from pydantic import BaseModel
from typing import Optional

# ------------------------------------------------------
# Productos - Base de Datos
# ------------------------------------------------------
class Producto(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class Producto_Update(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None 

products_list = []

# ------------------------------------------------------
# Usuarios - Base de Datos
# ------------------------------------------------------
class Usuarios(BaseModel):
    role: str 
    username: str 
    email: str 
    disabled: bool

class Usuarios_Update(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None 
    password: Optional[str] = None

class Usuarios_Security(Usuarios):
    password: str

users_list = {
    "lorenzo": {
        "role": 'ceo',
        "username": "lorenzopoggi",
        "email": "lorenzopoggi@gmail.com",
        "disabled": False,
        "password": '12345'
    },
    "sebastian": {
        "role": 'employee',
        "username": "sebastianerbino",
        "email": "erbinosebas@gmail.com",
        "disabled": False,
        "password": '12345'
    },
}