# mongoDB.py
from fastapi import APIRouter, HTTPException, status
from Backend.DataBase.database import db_client
from Backend.DataBase.Models.models import User
from Backend.DataBase.Schemas.schemas import user_schema

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Operacion para agregar usuarios a la base de datos MongoDB
@router.post("/")
async def add_users(user: User):
    # Convierto el modelo 'User' en un diccionario
    user_dict = dict(user)
    # Elimino el campo 'id' para que MongoDB lo genere automaticamente
    del user_dict['id']  
    # Inserto el usuario del modelo 'User' en la base de datos MongoDB y obtengo el ID generado
    id = db_client.local.users.insert_one(user_dict).inserted_id
    # Compruebo cual es el ID del usuario insertado y la operacion lo retorna como un diccionario
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    # Devuelo un objeto de tipo 'User' con los datos del nuevo usuario insertado
    return User(**new_user)