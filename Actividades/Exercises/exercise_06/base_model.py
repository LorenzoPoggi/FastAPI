# base_model.py — Sistema de Reservas de hoteles
# Base de Datos simulada para Hoteles y sus reservas

from pydantic import BaseModel

# ------------------------------------------------------
# Huespedes - Base de Datos
# ------------------------------------------------------

class Huespedes(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool
    role: str = 'user'

class Huespedes_Security(Huespedes):
    password: str 

lista_huespedes= {
    "lorenzo": {
        "id": 1,
        "username": "lorenzo",
        "email": "lorenzopoggi@gmail.com",
        "disabled": False,
        "role": "user",
        "password": '12345'
    }  
}

# ------------------------------------------------------
# Personal - Base de Datos
# ------------------------------------------------------

class Personal(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool
    role: str

class Personal_Security(Personal):
    password: str

lista_personal = {
    "pepe": {
        "id": 1,
        "username": "pepe",
        "email": "pepe@gmail.com",
        "disabled": False,
        "role": "admin",
        "password": '12345'
    },  
    "jorge": {
        "id": 1,
        "username": "jorge",
        "email": "jorge@gmail.com",
        "disabled": False,
        "role": "empleado",
        "password": '12345'
    }  
}

# ------------------------------------------------------
# Reservas - Base de Datos
# ------------------------------------------------------

class Reservas(BaseModel):
    id: int
    habitacion: int
    fecha_ingreso: str
    fecha_salida: str
    huesped: str

lista_reservas = []