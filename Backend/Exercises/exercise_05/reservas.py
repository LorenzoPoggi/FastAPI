# reservas.py
# API de un sistema basico para reservas de canchas 
# fastapi dev Exercises/exercise_05/reservas.py
from fastapi import FastAPI, Depends, HTTPException, status
from base_model import *
from exceptions import excepciones
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI(openapi_tags=['Reservas de Canchas'])

# ------------------------------------------------------
# Seguridad de Autenticación y Autorización
# ------------------------------------------------------

# Sistema de Autenticación
oauth2 = OAuth2PasswordBearer(tokenUrl='reservas/login')

#Algoritmo de Encriptación y Tocken de Acceso
ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 30
SECRET_KEY = '5e36b7f046a570f0ea534961a0c1e33cc87aab4504e1bfee53e63a08ed40b719'
crypt = CryptContext(schemes=['bcrypt'])

# Funciones para la busqueda de Usuarios 
def search_user_security(username: str):
    if username in database_users:
        return UserDB(**database_users[username])
    
def search_user(username: str):
    if username in database_users:
        return User(**database_users[username])
    
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
async def current_user(user: UserDB = Depends (auth_user)):
    if user.disabled:
        raise excepciones['usuario_deshabilitado']
    return user

# ------------------------------------------------------
# Operaciones del Sistema Backend
# ------------------------------------------------------

# Operacion para la autenticacion de usuarios registrados
@app.post('/reservas/login')
async def user_login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_security(form.username)
    if user is None:
        raise excepciones['usuario_no_encontrado']
    # Metodo de encriptación para verificar si las contraseñas son correctas
    if not crypt.verify(form.password, user.password):
        raise excepciones['contrasena_incorrecta']
    # Genero un Access Token con duracion de autenticacion
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expiration = datetime.now() + access_token_expire
    token = {'sub': user.username, 'exp': expiration}
    return {'access_token': jwt.encode(token, SECRET_KEY, algorithm= ALGORITHM), 'token_type': 'bearer'}

# Operacion para leer la lista de reservas
@app.get('/reservas')
async def user(user: User = Depends(current_user)):
    return database_reservas

# Operacion para crear una reserva
@app.post('/reservas')
async def reservar(nueva_reserva: Reserva, user: User = Depends(current_user)):
    for reserva in database_reservas:
        if reserva.id == nueva_reserva.id:
            raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST,
                                 detail={"Error": "La reserva ya existe"})
    nueva_reserva.usuario = user.username
    database_reservas.append(nueva_reserva)
    return nueva_reserva