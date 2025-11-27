# tienda.py - Control de productos en la Tienda
# El dueño quiere poder gestionar sus productos, consultarlos, actualizarlos y eliminarlos desde su sistema.
# fastapi dev Exercises/exercise_01/tienda.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entidad de la base de datos
class Productos (BaseModel):
    id: int
    name: str
    description: str
    value: float
    stock: bool

productos = []

# Operaciones para el control de stock 
@app.get('/productos')
async def general_view():
    return productos

@app.get('/productos/{id}')
async def products_view(id: int):
    for producto in productos:
        if producto.id == id:
            return producto
    return {'Error: producto no encontrado'}

@app.post('/productos')
async def add_products(new_product: Productos):
    for producto in productos:
        if new_product.id == producto.id:
            return {'Error: ya existe ese producto'}
    productos.append(new_product)
    return new_product

@app.put('/productos')
async def update_products(producto: Productos):
    found = False
    for index, saved_product in enumerate(productos):
        if saved_product.id == producto.id:
            productos[index] = producto
            found = True
    if not found:
        return {"Error": "No se ha actualizado el producto"}
    return producto

@app.delete('/productos/{id}')
async def delete_product(id: int):
    for producto in productos:
        if producto.id == id:
            productos.remove(producto)
            return {'Se ha eliminado el objeto'}