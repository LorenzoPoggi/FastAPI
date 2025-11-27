# http_status.py 
from fastapi import APIRouter, HTTPException
from Routers.creacion_API import *

router = APIRouter(tags=['HTTP Status'])

# -------------------------------------------------------
# Estados que devuelve el sistema luego de una operación
# -------------------------------------------------------

@router.post('/status', status_code= 201)
async def add_item(new_item: JSON):
    for item in item_list:
        if item.id == new_item.id:
            raise HTTPException (status_code= 204, detail= 'Ya existe el item')
            # return {"message": "Ya existe el item"}
    item_list.append(new_item)

    return new_item

http_status_codes_summary = [
    {
        "rango": "100 - 199",
        "nombre": "Informativo",
        "uso_comun": "Raramente se usan directamente. Indican una transferencia en curso.",
        "notas": "Las respuestas NO pueden tener cuerpo."
    },
    {
        "rango": "200 - 299",
        "nombre": "Éxito",
        "uso_comun": "Son los más comunes. Indican que la solicitud fue recibida, entendida y aceptada.",
        "ejemplos": "200 ('OK', por defecto), 201 ('Created', para nuevos registros), 204 ('No Content', sin cuerpo en la respuesta)."
    },
    {
        "rango": "300 - 399",
        "nombre": "Redirección",
        "uso_comun": "Indican que se necesita una acción adicional para completar la solicitud (por ejemplo, redirigir a otra URL).",
        "notas": "Pueden o no tener cuerpo, excepto 304 ('Not Modified'), que NO debe tenerlo."
    },
    {
        "rango": "400 - 499",
        "nombre": "Error del Cliente",
        "uso_comun": "Son muy comunes. Indican un error que parece haber sido causado por el cliente (por ejemplo, solicitud incorrecta o recurso no encontrado).",
        "ejemplos": "404 ('Not Found'), 400 (para errores genéricos del cliente)."
    },
    {
        "rango": "500 - 599",
        "nombre": "Error del Servidor",
        "uso_comun": "Raramente se usan directamente por el desarrollador. Indican un fallo por parte del servidor al procesar una solicitud válida.",
        "notas": "Suelen ser devueltos automáticamente ante fallos en la aplicación o el servidor."
    }
]