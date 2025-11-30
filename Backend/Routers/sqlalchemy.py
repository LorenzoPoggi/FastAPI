# sqlachemy.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from DataBase.SQLAlchemy.database import get_db, engine, Base 
from DataBase.SQLAlchemy.Models.models import *
from DataBase.SQLAlchemy.Schemas.schemas import *
from typing import List

# Inicializa las tablas en la base de datos 
Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["SQLAlchemy"],
                   prefix="/sqlalchemy",
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# ----------------------------------------------------
# Helpers (Ayudantes)
# ----------------------------------------------------

# Funcion para la busqueda de usuarios por email
def get_user_by_email(db: Session, email: str) -> User | None:
    # Usamos User que es el nombre de la clase del modelo
    return db.query(User).filter(User.email == email).first()

# Funcion para la busqueda de usuarios por id
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# ----------------------------------------------------
# Operaciones CRUD para Usuarios
# ----------------------------------------------------

# Operación para agregar usuarios
@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifico si el email ya existe
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    # Encriptacion de la contraseña (simulada)
    hashed_password = user.password + "notreallyhashed"
    # Creo el usuario en la base de datos
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        username=user.email.split('@')[0] 
    )
    # Agregar y confirma los cambios
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Devuelvo el usuario creado 
    return db_user

# Operación para obtener todos los usuarios
@router.get("/users/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    # Devuelvo todos los usuarios
    return db.query(User).all()

# Operación para obtener un usuario con su ID
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # Buscamos y filtramos el usuario por el id
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Devuelvo el usuario
    return db_user

# Operación para actualizar los datos de un usuario (Usando UserBase para no requerir la contraseña)
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    # Buscamos y filtramos el usuario por el id
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Si se intenta cambiar el email, verificar si el nuevo email ya existe en otro usuario
    if db_user.email != user.email and get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="El nuevo email ya está registrado por otro usuario")
    # Actualiza los campos
    db_user.email = user.email
    db_user.username = user.email.split('@')[0] # Actualiza el username basado en el nuevo email
    # Confirma los cambios
    db.commit()
    db.refresh(db_user)
    # Devuelvo el usuario con los datos actualizados
    return db_user

# Operación para eliminar un usuario
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Buscamos y filtramos el usuario por el id
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Elimino el usuario de la base de datos
    db.delete(db_user)
    db.commit()
    return {}

# ----------------------------------------------------
# Operaciones CRUD para Items
# ----------------------------------------------------

# Operación para crear un nuevo item para un usuario especifico
@router.post("/users/{user_id}/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    # Verificar si el owner existe
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="El propietario del Item no fue encontrado")
    # Crear la instancia del modelo de Item
    db_item = Item(**item.model_dump(), owner_id=user_id)
    # Agregar y confirmar la transacción
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Devuelvo el item nuevo creado para un usuario
    return db_item

# Operación para obtener todos los items
@router.get("/items/", response_model=List[Item])
async def read_items(db: Session = Depends(get_db)):
    # Devuelvo todos los items
    return db.query(Item).all()

# Operación para obtener un item por ID
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    # Buscamos y filtramos el item por el id
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return db_item

# Operación para actualizar un item
@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemBase, db: Session = Depends(get_db)):
    # Buscamos y filtramos el item por el id
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    # Actualiza los campos
    db_item.title = item.title
    db_item.description = item.description
    # Confirma los cambios
    db.commit()
    db.refresh(db_item)
    # Devuelvo el item actualizado
    return db_item

# Operación para eliminar un item
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    # Buscamos y filtramos el item por el id
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    # Elimino el item de la base de datos
    db.delete(db_item)
    db.commit()
    return {}