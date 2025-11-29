# mongoDB.py

from fastapi import APIRouter, HTTPException, status
from DataBase.database import db_client
from DataBase.Models.models import User
from DataBase.Schemas.schemas import user_schema, users_schema
from bson import ObjectId

router = APIRouter(tags=["MongoDB"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# ----------------------------------------------------
# Busqueda de usuarios en la base de datos MongoDB
# ----------------------------------------------------

# Operacion para obtener todos los usuarios de la base de datos MongoDB
def search_user(field: str, key):
    # Busco el usuario en la base de datos segun el campo y la clave proporcionados
    try:
        # Si se encuentra el usuario, retorno el esquema del usuario 
        user = db_client.Usuarios.find_one({field: key})
        return User(**user_schema(user))
    except: 
        # Si no se encuentra el usuario, retorno None
        return {"error": "No se ha encontrado el usuario"} 
    
# ----------------------------------------------------
# Operaciones del sistema Backend
# ----------------------------------------------------

# Operacion para agregar usuarios a la base de datos MongoDB
@router.post("/mongodb")
async def add_users(user: User):
    # Verifico si el email del usuario a guardar ya existe en la base de datos 
    if type (search_user('email', user.email)) == User:
        raise HTTPException(status_code=400, detail="El usuario ya existe en la base de datos")
    # Convierto el modelo 'User' en un diccionario
    user_dict = dict(user)
    # Elimino el campo 'id' para que MongoDB lo genere automaticamente
    del user_dict['id']  
    # Inserto el usuario del modelo 'User' en la base de datos MongoDB y obtengo el ID generado
    id = db_client.Usuarios.insert_one(user_dict).inserted_id
    # Compruebo cual es el ID del usuario insertado y la operacion lo retorna como un diccionario
    new_user = user_schema(db_client.Usuarios.find_one({"_id": id}))
    # Devuelo un objeto de tipo 'User' con los datos del nuevo usuario insertado
    return User(**new_user)

# Operacion para obtener todos los usuarios de la base de datos MongoDB por lista
@router.get("/mongodb", response_model=list[User])
async def get_users():
    # Retorno todos los usuarios de la base de datos 
    return users_schema(db_client.Usuarios.find())

# Operacion para obtener un usuario con su ID
@router.get("/mongodb/{id}")
async def get_user(id: str):
    # Retorno el usuario que coincide con el ID proporcionado
    return search_user("_id", ObjectId(id))

# Operacion para eliminar un usuario de la base de datos MongoDB por su ID
@router.delete("/mongodb/{id}")
async def delete_user(id: str, status_code= status.HTTP_204_NO_CONTENT):
    # Busco al usuario en la base de datos MongoDB por su ID y lo elimino
    found = db_client.Usuarios.find_one_and_delete({"_id": ObjectId(id)})
    # Si no lo encuentro devuelvo un error 
    if not found:
        return {'error': 'no se ha eliminado al usuario'}
    
# Operacion para actualizar un usuario de la base de datos MongoDB
@router.put('/', response_model=User)
async def replace_user(user: User):
    # Convierto el modelo 'User' en un diccionario
    user_dict = dict(user)
    # Eliminamos el parametro de ID porque no se puede eliminar 
    del user_dict['id']
    try:
        # Busco al usuario en la base de datos y reemplazo los datos a partir del diccionario del user
        db_client.Usuarios.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        # Devuelvo un error si no se pudo hacer la operacion
        return {"error": "No se ha actualizado el usuario"}
    # Devuelvo al usuario con los datos actualizados a partir de us ID
    return search_user("_id", ObjectId(user.id))  