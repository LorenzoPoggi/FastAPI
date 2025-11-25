# base_model.py — Sistema de Reservas
# Base de Datos simulada para Usuarios y Reservas

from pydantic import BaseModel
from typing import Optional

# -----------------------------------------------------------
# Usuarios (para autenticación con JWT)
# -----------------------------------------------------------

class User(BaseModel):
    username: str
    email: str
    fullname: str
    disabled: bool = False

class UserDB(User):
    password: str

database_users = {
    "lorenzo": {
        "username": "lorenzopoggi",
        "email": "lorenzopoggi@gmail.com",
        "fullname": "Lorenzo Poggi",
        "disabled": False,
        "password": "12345"
    },
    "sofia": {
        "username": "sofiagomez",
        "email": "sofia@gmail.com",
        "fullname": "Sofía Gómez",
        "disabled": False,
        "password": "abc123"
    },
    "admin": {
        "username": "admin",
        "email": "admin@reservas.com",
        "fullname": "Administrador",
        "disabled": False,
        "password": "adminpass"
    }
}

# -----------------------------------------------------------
# Reservas (solo para el ejercicio A)
# -----------------------------------------------------------

class Reserva(BaseModel):
    id: int
    usuario: str        # username del usuario que reserva
    espacio: str        # cancha / sala / recurso
    fecha: str          # ejemplo: "2025-01-15"
    hora: str           # ejemplo: "18:30"

database_reservas = []