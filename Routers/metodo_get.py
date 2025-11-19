# metodo_get.py
from fastapi import APIRouter
from Routers.creacion_API import item_list, JSON

router = APIRouter(tags=['Get'])

# ----------------------------------------------------
# Rutas GET básicas (leer datos)
# ----------------------------------------------------

@router.get('/')
async def index():
    return 'Hola Mundo'

@router.get('/items')
async def view_items():
    return item_list

@router.get('/items/{id}')
async def view_item_id(id: int):
    for item in item_list:
        if item.id == id:
            return item
    return {"error": "Item no encontrado"}
