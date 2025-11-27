# metodo_post.py
from fastapi import APIRouter
from Routers.creacion_API import item_list, JSON

router = APIRouter(tags=['Post'])

# ----------------------------------------------------
# Rutas POST básicas (agregar datos)
# ----------------------------------------------------

@router.post('/items')
async def add_item(new_item: JSON):
    for item in item_list:
        if item.id == new_item.id:
            return {"message": "Ya existe el item"}
    item_list.append(new_item)

    return new_item