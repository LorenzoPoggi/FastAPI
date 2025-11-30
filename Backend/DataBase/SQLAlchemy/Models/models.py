# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from DataBase.SQLAlchemy.database import Base

class User(Base):
    __tablename__ = "Usuarios"

    # La columna 'id' es la clave primaria y se auto-incrementa
    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default= True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacion: El usuario tiene una lista de Items
    items = relationship('Item', back_populates='owner')

class Item(Base):
    __tablename__ = "Items"

    # La columna 'id' es la clave primaria y se auto-incrementa
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('Usuarios.id')) 

    # Relacion: El item pertenece a un solo Usuario (owner)
    owner = relationship('User', back_populates='items')
    # back_populates establece la relacion bidireccional entre User.items y Item.owner