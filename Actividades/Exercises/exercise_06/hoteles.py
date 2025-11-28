# hoteles.py - Sistema de Gestión de Reservas en Hoteles
# API para gestionar reservas de un hotel. Los users pueden registrarse y proteger sus datos via JWT e inspeccionar sus reservas.
# fastapi dev Exercises/exercise_06/hoteles.py 

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from exceptions import excepciones
from base_model import *

app = FastAPI(openapi_tags=[{"name": "Reserva de Hoteles"}])

# ------------------------------------------------------
# Seguridad de Autenticación y Autorización
# ------------------------------------------------------

# Sistema de Autenticacion 
oauth2 = OAuth2PasswordBearer(tokenUrl="hotel/login")

# Algoritimo de Encriptacion y Tocken de Acceso
ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 30
SECRET_KEY = '5e36b7f046a570f0ea534961a0c1e33cc87aab4504e1bfee53e63a08ed40b719'
crypt = CryptContext(schemes=['bcrypt'])

# Funciones para la busqueda de usuarios
def search_user (username: str):
    if username in lista_huespedes:
        return Huespedes(**lista_huespedes[username])
    elif username in lista_personal:
        return Personal(**lista_personal[username])

def search_user_security(username: str):
    if username in lista_huespedes:
        return Huespedes_Security(**lista_huespedes[username])
    elif username in lista_personal:
        return Personal_Security(**lista_personal[username])
    
# Criterio para encontrar al usuario autenticado 
async def auth_user(token: str = Depends(oauth2)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise excepciones['no_autorizado']
    except JWTError:
        raise excepciones['no_autorizado']
    return search_user_security(username)

# Criterio de Dependencia y Autenticacion
async def current_user(user = Depends(auth_user)):
    if user.disabled:
        raise excepciones['usuario_deshabilitado']
    return user

# ------------------------------------------------------
# Operaciones del Sistema Backend
# ------------------------------------------------------

# Operacion para el registro de nuevos usuarios
@app.post('/hotel/register')
async def user_register(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_security(form.username)
    if form.username in lista_huespedes or form.username in lista_personal:
        raise excepciones["usuario_ya_registrado"]
    
    hashed_password = crypt.hash(form.password)
    new_user = {
        "id": len(lista_huespedes) + len(lista_personal) + 1,
        "username": form.username,
        "email": form.username + "@gmail.com",
        "disabled": False,
        "role": "user",
        "password": hashed_password
    }
    lista_huespedes[form.username] = new_user
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expiration = datetime.now() + access_token_expires
    token = {'sub': form.username, 'exp': expiration}
    return {'access_token': jwt.encode(token, SECRET_KEY, algorithm= ALGORITHM),
             'token_type': 'bearer'}

# Operacion para la autenticacion de usuarios registrados
@app.post('/hotel/login')
async def user_login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_security(form.username)
    if user is None:
        raise excepciones['usuario_no_encontrado']
    if not crypt.verify(form.password, user.password):
        raise excepciones['contrasena_incorrecta']
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expiration = datetime.now() + access_token_expires
    token = {'sub': user.username, 'exp': expiration}
    return {'access_token': jwt.encode(token, SECRET_KEY, algorithm= ALGORITHM),
             'token_type': 'bearer'}

# Operacion para que huespedes creen sus reservas y se guarden en la base de datos
@app.post('/hotel/reservas')
async def create_reservation(reservation_data: dict, user: Huespedes_Security = Depends(current_user)):
    reserva_id = len(lista_reservas) + 1
    reserva = {
        "reservation_id": reserva_id,
        "user": user.username,
        "data": reservation_data
    }
    lista_reservas.append(reserva)
    return {"Mensaje": f"Reserva creada para el usuario {user.username}", "Reserva": reserva}

# Operacion para que huespedes vean sus reservas
@app.get('/hotel/reservas')
async def view_reservations(user: Huespedes_Security = Depends(current_user)):
    reservas_usuario = [r for r in lista_reservas if r["user"] == user.username]
    return {"reservas": reservas_usuario}

# Operacion para que el administrador vea todas las reservas
@app.get('/hotel/reservas/todas')
async def view_all_reservations(user = Depends(current_user)):
    if user.role != 'admin':
        raise excepciones['no_tiene_permisos']
    return {"Mensaje": "Lista de todas las reservas del hotel", "Lista": lista_reservas}

# Operacion para que un administrador actualice una reserva existente
@app.put('/hotel/reservas/{reservation_id}')
async def update_reservation(reservation_id: int, updated_data: dict, user: Personal_Security = Depends(current_user)):
    if user.role != 'admin':
        raise excepciones['no_tiene_permisos']
    for reserva in lista_reservas:
        if reserva["reservation_id"] == reservation_id:
            reserva["data"] = updated_data
            return {"Mensaje": f"Reserva {reservation_id} actualizada por el administrador {user.username}", "Reserva": reserva}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

# Operacion para que un administrador elimine una reserva
@app.delete('/hotel/reservas/{reservation_id}')
async def delete_reservation(reservation_id: int, user: Personal_Security = Depends(current_user)):
    if user.role != 'admin':
        raise excepciones['no_tiene_permisos']
    for index, reserva in enumerate(lista_reservas):
        if reserva["reservation_id"] == reservation_id:
            del lista_reservas[index]
            return {"Mensaje": f"Reserva {reservation_id} eliminada por el administrador {user.username}"}  