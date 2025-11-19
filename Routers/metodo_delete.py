# metodo_delete.py
from fastapi import APIRouter
from Routers.creacion_API import item_list, JSON

router = APIRouter(tags=['Delete'])

# ----------------------------------------------------
# Rutas DELETE básicas (eliminar datos)
# ----------------------------------------------------

@router.delete('/items/{id}')
async def eliminate_item(id:int):
    for item in item_list:
        if item.id == id:
            item_list.remove(item)
    return {"message: item eliminado"}

