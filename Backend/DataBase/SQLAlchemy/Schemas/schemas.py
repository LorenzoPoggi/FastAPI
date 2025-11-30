# schemas.py
from pydantic import BaseModel, EmailStr 
from typing import Optional, List
from datetime import datetime 

# ----------------------------------------------------
# Items Schemas
# ----------------------------------------------------

# Obtiene bases comunes 
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

# Crear nuevos registros 
class ItemCreate(ItemBase):
    pass

# Datos de salida 
class Item(ItemBase):
    id: int
    owner_id: int
    # Clase para convertir de objeto sqlalchemy a este modelo, FastAPI lo interpreta 
    class Config:
        from_attributes = True 

# ----------------------------------------------------
# Users Schemas
# ----------------------------------------------------

# Obtiene bases comunes 
class UserBase(BaseModel):
    email: EmailStr

# Crear nuevos registros 
class UserCreate(UserBase):
    password: str

# Datos de salida 
class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    items: List[Item] = []
    # Clase para convertir de objeto sqlalchemy a este modelo, FastAPI lo interpreta 
    class Config: 
        from_attributes = True 