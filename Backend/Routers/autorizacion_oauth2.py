# autorizacion_oauth2.py
from fastapi import APIRouter, Depends, HTTPException, status
from Routers.creacion_API import User, UserDB, database_users
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=['Autorizacion Oauth2'])

# Sistema de Autenticacion
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

# Funcion para la busqueda de usuarios en la base de datos (simulada) tipo UserDB
def search_user_db(username: str):
    if username in database_users:
        return UserDB(**database_users[username])
    
# Funcion para la creacion de usuarios en la base de datos (simulada) tipo User
def search_user(username: str):
    if username in database_users:
        return User(**database_users[username])
    
# Criterio de Dependencia 
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail= {'Error:': 'Credenciales de autenticacion invalidas'}, 
                            headers= {'WWW-Authenticate': 'Bearer'})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= {'Error:': 'Usuario inactivo'})
    return user 
    
# Operacion para la autenticacion de usuarios registrados
@router.post('/login')
async def user_login(form: OAuth2PasswordRequestForm = Depends()):
    # Busco el usuario en la base de datos (simulada)
    username= database_users.get(form.username) 
    if not username:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= {'Error': 'No se encontro al usuario'})
    # Verifico la contraseña del usuario 
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= {'Error:': 'Contraseña incorrecta'})
    # Devuelvo un Access Token
    return {'access_token': user.username, 'token_type': 'bearer'}

# Operacion para obtener datos del usuario
@router.get('/login/me')
async def my_user(user: User = Depends(current_user)):
    return user 