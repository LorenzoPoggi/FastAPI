# inventario.py - Sistema de Gestión de Inventario
# API para gestionar productos del inventario. El sistema debe validar que usuarios autenticados puedan modificar o crear productos
# fastapi dev Exercises/exercise_04/inventario.py 

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from base_model import *

app = FastAPI(openapi_tags=[{"name": "Inventory"}])

# ------------------------------------------------------
# Seguridad de Autenticación y Autorización
# ------------------------------------------------------

# Sistema de Autenticacion
oauth2 = OAuth2PasswordBearer(tokenUrl='inventory')

# Funciones para la busqueda de Usuarios 
def search_user(username: str):
    if username in users_list:
        return Usuarios(**users_list[username])

def search_user_security(username: str):
    if username in users_list:
        return Usuarios_Security(**users_list[username])
    
# Criterios de Dependencia y Autenticacion
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= 'Credenciales inválidas')
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= 'Usuario deshabilitado')
    return user

# ------------------------------------------------------
# Operaciones del Sistema Backend
# ------------------------------------------------------

# Operacion para ver lista de empleados
@app.get('/sistema/usuarios')
async def list_users():
    return {"Lista de Usuarios": users_list}

# Operacion para obtener datos del usuario 
@app.get('/sistema/usuarios/{username}')
async def users_information(username: str, user: Usuarios = Depends(current_user)):
    if username in users_list:
        return {"Informacion del usuario": users_list[username]}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= 'Usuario no encontrado')

# Operacion para que el CEO vea la lista de empleados
@app.get('/sistema/usuarios/inventario')
async def products_view(user: Usuarios = Depends(current_user)):
    if user.role != 'ceo':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='El CEO puede acceder a la Lista de Productos')
    return {"Lista de Productos": products_list}

# Operacion para la autenticacion de usuarios registrados
@app.post('/sistema/usuarios')
async def users_login(form: OAuth2PasswordRequestForm = Depends()):
    username = users_list.get(form.username)
    if not username:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= 'Usuario no encontrado')
    user = search_user_security(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= 'Contraseña incorrecta')
    return {'access_token': user.username, 'token_type': 'bearer'}

# Operacion para registrar un nuevo usuario
@app.post('/sistema/usuarios/registro')
async def users_register(new_user: Usuarios_Security):
    for user_data in users_list.values():
        if new_user.username == user_data['username']:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= 'Username ya registrado')
        if new_user.email == user_data['email']:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= 'Email ya registrado')
    users_list[new_user.username] = new_user.model_dump()
    return {'message':'Usuario nuevo registrado', 'usuario': new_user}
        
# Operacion para actualizar datos de un usuario autenticado 
@app.put('/sistema/usuarios/actualizar')
async def users_update(data_update: Usuarios_Update, user: Usuarios = Depends(current_user)):
    if user.username not in users_list:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= 'Usuario no encontrado')
    saved_user = users_list[user.username]
    if data_update.email:
        saved_user['email'] = data_update.email
    if data_update.password:
        saved_user['password'] = data_update.password
    users_list[user.username] = saved_user
    return {'message': 'Datos actualizados correctamente', 'usuario': saved_user}

# Operacion para eliminar usuarios 
@app.delete('/sistema/usuarios/eliminacion/{username}')
async def users_delete(username: str, user: Usuarios = Depends(current_user)):
    if user.role != 'ceo':
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail= 'No tiene permisos')
    if username not in users_list:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= 'Usuario no encontrado')
    if username == user.username:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                                detail= 'No sea puede eliminar al CEO')
    objective_username = Usuarios(**users_list[username])
    if objective_username.role == 'ceo':
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= 'No sea pueden eliminar CEOS')
    del users_list[username]
    return {'message':'Usuario eliminado con éxito', 'usario eliminado': username}