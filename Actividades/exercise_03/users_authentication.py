# users_authentication.py - Sistema de Acceso y Gestión de Usuarios
# API que gestiona la autenticación y permisos de usuarios en una plataforma interna de la empresa, utilizando un sistema de inicio de sesión con tokens.
# fastapi dev Exercises/exercise_03/users_authentication.py 

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from base_model import *

app = FastAPI(openapi_tags= ['Users Authentication'])

# ------------------------------------------------------
# Seguridad de Autenticación y Autorización
# ------------------------------------------------------

# Sistema de Autenticacion
oauth2 = OAuth2PasswordBearer(tokenUrl='users')

# Funcion para la busqueda de Usuarios en la db Usuarios_Security
def search_user_db(username: str):
    if username in Lista_Empleados:
        return Usuarios_Security(**Lista_Empleados[username])

# Funcion para la bsuqueda de Usuarios en la db Usuarios
def search_user(username: str):
    if username in Lista_Empleados:
        return Usuarios(**Lista_Empleados[username])

# Criterio de Dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= {'Error': 'Credenciales de autenticacion invalidas'},
                            headers= {'WWW-Authenticate': 'Bearer'})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= {'Error': 'Usuario Inactivo'})
    return user

# ------------------------------------------------------
# Operaciones dentro del Sistema Backend
# ------------------------------------------------------

# Operacion para que el CEO vea la lista de empleados
@app.get('/users')
async def users_view(user: Usuarios = Depends(current_user)):
    if user.role != 'ceo':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= {'Error': 'Acceso denegado'})
    {"message": "Lista de empleados", "usuario": Lista_Empleados}

# Operacion para obtener datos del usuario
@app.get('/users/me')
async def own_users(user: Usuarios = Depends(current_user)):
    {"message": "Datos del usuario", "usuario": user}

# Operacion para la autenticacion de usuarios registrados
@app.post('/users')
async def users_login(form: OAuth2PasswordRequestForm = Depends()):
    username = Lista_Empleados.get(form.username)
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'Error': 'No se encontro al usuario'})
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'Error':'Contraseña incorrecta'})
    return {'access_token': user.username, 'token_type': 'bearer'}

# Operacion para registrar un nuevo usuario
@app.post('/users/register')
async def users_register(new_user: Usuarios_Security):
    for user_data in Lista_Empleados.values():
        if new_user.username == user_data['username']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail= {'Error':'Username ya registrado'})
        if new_user.email == user_data['email']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail= {'Error':'Email ya registrado'})
    Lista_Empleados[new_user.username] = new_user.model_dump()
    return {"message": "Usuario nuevo registrado", "usuario": new_user}

# Operacion para actualizar datos de un usuario autenticado 
@app.put('/users/me')
async def users_update(data_update: Usuarios_Update, user: Usuarios = Depends(current_user)):
    if user.username not in Lista_Empleados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'Error':'Usuario no encontrado'})
    saved_user = Lista_Empleados[user.username]
    if data_update.fullname:
        saved_user['fullname'] = data_update.fullname
    if data_update.email:
        saved_user['email'] = data_update.email
    if data_update.password:
        saved_user['password'] = data_update.password
    Lista_Empleados[user.username] = saved_user
    return {"message": "Datos actualizados correctamente", "usuario": saved_user}