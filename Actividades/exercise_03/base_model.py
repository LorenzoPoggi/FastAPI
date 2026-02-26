# base_model.py - Sistema de Acceso y Gestión de Usuarios
# Base de Datos simulada

# ------------------------------------------------------
# Entidades y Bases de Datos (simulada) para Usuarios
# ------------------------------------------------------

from pydantic import BaseModel
from typing import Optional

class Usuarios(BaseModel):
    role: str
    username: str
    fullname: str
    email: str
    disabled: bool

class Usuarios_Security(Usuarios):
    password: str

class Usuarios_Update(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

Lista_Empleados = {
    "lorenzo": {
        "role": 'ceo',
        "username": "lorenzopoggi",
        "fullname": "Lorenzo Poggi Janin",
        "email": "lorenzopoggi@gmail.com",
        "disabled": False,
        "password": '12345'
    },
    "sebastian": {
        "role": 'employee',
        "username": "sebastianerbino",
        "fullname": "Sebastian Erbino",
        "email": "erbinosebas@gmail.com",
        "disabled": False,
        "password": '12345'
    },
    "tiziano": {
        "role": 'employee',
        "username": "tizianopatella",
        "fullname": "Tiziano Patella",
        "email": "titipatella@gmail.com",
        "disabled": True,
        "password": '12345'
    },
}