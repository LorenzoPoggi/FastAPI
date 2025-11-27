# autenticacion_jwt.py
from fastapi import APIRouter, Depends, HTTPException, status
from Routers.creacion_API import User_2, UserDB_2, database_users_2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(tags=['Autenticación Oauth2 JWT'])

# Sistema de Autenticacion
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

# Algoritmo de Encriptación y Tocken de Acceso
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
# 'openssl rand -hex 32' para recibir una key segura 
SECRET_KEY = 'e2cadd35402cb270f7c256664f62b610dd9199c964a9fb616aef05f9a8ac5494'
crypt = CryptContext(schemes="bcrypt")

# Funcion para la busqueda de usuarios en la base de datos (simulada)
def search_user_db(username: str):
    # Verifico si el username existe en la base de datos
    if username in database_users_2:
        # Devuelvo un username del modelo de la base de datos (incluye password hasheada)
        return UserDB_2(**database_users_2[username])

# Funcion para la creacion de usuarios en la base de datos (simulada) tipo User
def search_user(username: str):
    # Verifico si el username existe en la base de datos
    if username in database_users_2:
        # Devuelvo un username del modelo de la base de datos (sin password)
        return User_2(**database_users_2[username])
    
# Criterio para encontrar al usuario autenticado
async def auth_user(token : str = Depends(oauth2)):
    # Excepción estándar para devolver si falla la autenticación
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail= {'Error:': 'Credenciales de autenticacion invalidas'}, 
                            headers= {'WWW-Authenticate': 'Bearer'})
    try:
        # Decodifico el token usando la SECRET_KEY ALGORITMO para obtener el payload 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # dict con datos del usuario dentro del token
        # Extraigo el username desde el campo 'sub' del token
        username = payload.get("sub")
        if username is None:
            raise exception
    except JWTError: 
        raise  exception
    return search_user(username)
        
# Criterio de Dependencia 
async def current_user(user: User_2 = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= {'Error:': 'Usuario inactivo'})
    return user 
     
# Operacion para la autenticacion de usuarios registrados
@router.post('/login')
async def user_login(form: OAuth2PasswordRequestForm = Depends()):
    # Busco el usuario en la base de datos (simulada)
    username= database_users_2.get(form.username) 
    if not username:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= {'Error': 'No se encontro al usuario'})
    # Metodo de encriptación para verificar si las contraseñas son correctas
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= {'Error:': 'Contraseña incorrecta'})
    # Genero un Access Token con duracion de autenticacion
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expiration = datetime.now() + access_token_expire
    access_token = {'sub': user.username, 
                    'exp': expiration}
    # Devuelvo ese access tocken encriptado y hasheado
    return {'access_token': jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), 'token_type': 'bearer'}

# Operacion para obtener datos del usuario
@router.get('/login/me')
async def my_user(user: User_2 = Depends(current_user)):
    return user 