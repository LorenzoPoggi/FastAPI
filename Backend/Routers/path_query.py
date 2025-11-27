# path_query.py
from fastapi import APIRouter
from Routers.creacion_API import item_list, Regiones

router = APIRouter(tags=['Path and Query'])

# ----------------------------------------------------
# Rutas con Query Parameters
# ----------------------------------------------------

@router.get('/items/filter')
async def filtrar_items(stock: bool = None, max_price: int = None):
    results = item_list

    if stock is not None:
        results = [item for item in results if item.stock == stock]
    if max_price is not None:
        results = [item for item in results if item.price <= max_price]

    return results

# ----------------------------------------------------
# Rutas con Path Parameters (Enum)
# ----------------------------------------------------

@router.get('/lugar')
async def lugar():
    return 'Escriba un pais en el Path'

@router.get('/lugar/{pais}')
async def lugar_pais(pais: Regiones):
    if pais is Regiones.Europa:
        return f'Welcome to {pais.value}'
    elif pais is Regiones.America:
        return f'Bienvenido a {pais.value}'
    elif pais is Regiones.Oceania:
        return f'Willkommen zu {pais.value}'
