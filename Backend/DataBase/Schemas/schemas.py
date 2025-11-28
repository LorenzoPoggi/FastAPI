# schemas.py
# Archivo para operaciones entre modelos de datos y la base de datos MongoDB

def user_schema(user) -> dict: # devuelve un diccionario
    # Convierte el usuario recibido de la base de datos en un diccionario
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }