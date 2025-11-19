# metodo_put.py
from fastapi import APIRouter
from Routers.creacion_API import item_list, JSON

router = APIRouter(tags=['Put'])

# ----------------------------------------------------
# Rutas PUT básicas (actualizar datos)
# ----------------------------------------------------

@router.put('/items')
async def update_item(item: JSON):

    found = False

    for index, saved_item in enumerate(item_list):
        if saved_item.id == item.id:
            item_list[index] = item
            found = True
    
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return item