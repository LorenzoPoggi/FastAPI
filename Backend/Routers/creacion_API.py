# creacion_API.py
from enum import Enum
from pydantic import BaseModel

# --------------------------------------------------------
# Entidades y Bases de Datos (simuladas) para Operaciones
# --------------------------------------------------------

# Modelo de entidad
class JSON(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: bool

# Base de datos simulada
item_list = [
    JSON(id=1, name="Jugo", description="Naranja", price=10, stock=True),
    JSON(id=2, name="Pepsi", description="Gaseosa", price=20, stock=False),
    JSON(id=3, name="Agua", description="Natural", price=5, stock=True)
]

# Enumeración de regiones
class Regiones(str, Enum):
    Europa = "Reino Unido"
    America = "Argentina"
    Oceania = "Australia"

# ------------------------------------------------------
# Entidades y Bases de Datos (simulada) para Usuarios
# ------------------------------------------------------

class User(BaseModel):
    username: str
    email: str
    fullname: str
    disabled: bool

class UserDB (User):
    password: str
    
database_users = {
    "lorenzo": {
        "username": "lorenzopoggi",
        "email": "lorenzopoggi@gmail.com",
        "fullname": "Lorenzo Poggi",
        "disabled": True,
        "password": '12345'
    },
    "santos": {
        "username": "santos",
        "email": "santos@gmail.com",
        "fullname": "Santos",
        "disabled": False,
        "password": '67890'
    },
    "pepe": {
        "username": "pepe",
        "email": "pepe@gmail.com",
        "fullname": "Pepe",
        "disabled": True,
        "password": '98765'
    }
}

# -----------------------------------------------------------
# Entidades y Bases de Datos (simulada) para Usuarios en JWT
# -----------------------------------------------------------

class User_2(BaseModel):
    username: str
    email: str
    fullname: str
    disabled: bool

class UserDB_2(User_2):
    password: str
    
database_users_2 = {
    "lorenzo": {
        "username": "lorenzopoggi",
        "email": "lorenzopoggi@gmail.com",
        "fullname": "Lorenzo Poggi",
        "disabled": True,
        "password": '12345'
    },
    "santos": {
        "username": "santos",
        "email": "santos@gmail.com",
        "fullname": "Santos",
        "disabled": False,
        "password": '67890'
    },
    "pepe": {
        "username": "pepe",
        "email": "pepe@gmail.com",
        "fullname": "Pepe",
        "disabled": True,
        "password": '98765'
    }
}