# schemas.py
# Archivo para operaciones entre modelos de datos y la base de datos MongoDB

def user_schema(user) -> dict: # devuelve un diccionario de un solo usuario
    # Convierte el usuario recibido de la base de datos en un diccionario
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

def users_schema(users) -> list: # devuelve una lista
    # Convierte una lista de usuarios recibidos de la base de datos en una lista de diccionarios
    return [user_schema(user) for user in users]