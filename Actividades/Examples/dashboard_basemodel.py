"""
dashboard_basemodel.py

Dashboard ejemplo 2 — Uso de Pydantic `BaseModel`.

Objetivo: mostrar cómo definir modelos con Pydantic (BaseModel) y usarlos
en rutas POST/GET. Incluye ejemplos detallados línea a línea.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict

# ------------------------------------------------------------------
# Definición del modelo de datos con Pydantic
# ------------------------------------------------------------------

class Item(BaseModel):
    """Modelo de ejemplo para un recurso 'Item'.

    - `name`: nombre del item (str)
    - `description`: campo opcional
    - `price`: precio como float
    - `metadata`: diccionario opcional con datos extra
    """
    name: str
    description: Optional[str] = None
    price: float
    metadata: Optional[Dict[str, str]] = None


# Creamos la app FastAPI
app = FastAPI()

# Pequeña 'base de datos' en memoria (dict) para ejemplo
DB: Dict[str, dict] = {}


@app.get("/basemodel/dashboard", response_class=HTMLResponse)
async def basemodel_dashboard():
    """Vista principal del dashboard que demuestra envío y visualización

    - Permite crear Items con fetch (POST JSON)
    - Muestra lista actual de Items desde el "DB" en memoria (GET)
    """
    html = """
    <html>
      <head><meta charset='utf-8'/><title>Dashboard BaseModel</title></head>
      <body>
        <h1>Dashboard — BaseModel</h1>

        <section>
          <h2>Crear Item (POST JSON usando fetch)</h2>
          <p>Nombre: <input id="name"/></p>
          <p>Precio: <input id="price"/></p>
          <p><button id="btnCreate">Crear</button></p>
        </section>

        <section>
          <h2>Items guardados</h2>
          <pre id="items"></pre>
        </section>

        <script>
        async function refresh(){
          const res = await fetch('/basemodel/items');
          const items = await res.json();
          document.getElementById('items').textContent = JSON.stringify(items, null, 2);
        }
        document.getElementById('btnCreate').addEventListener('click', async ()=>{
          const name = document.getElementById('name').value || 'sin-nombre';
          const price = parseFloat(document.getElementById('price').value || '0');
          const payload = { name, price };
          const res = await fetch('/basemodel/items', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
          });
          const data = await res.json();
          console.log(data);
          await refresh();
        });
        // refrescar al cargar
        refresh();
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post('/basemodel/items')
async def create_item(item: Item):
    """Crear un Item usando Pydantic para validación automática.

    - FastAPI extrae JSON del cuerpo y lo valida contra `Item`.
    - Si faltan campos o tipos incorrectos, FastAPI devuelve 422 automáticamente.
    """
    # Guardamos en memoria usando nombre como clave (ejemplo simple)
    DB[item.name] = item.model_dump()
    return JSONResponse({"created": True, "item": item.model_dump()})


@app.get('/basemodel/items')
async def list_items():
    """Devuelve todos los items guardados en memoria."""
    return JSONResponse(DB)


# Notas para aprender (línea a línea):
# - `class Item(BaseModel)`: define el esquema. FastAPI usará esto para validar JSON.
# - `create_item(item: Item)`: FastAPI convierte el body JSON al objeto `Item`.
# - `item.model_dump()`: método de Pydantic v2 para obtener dict serializable del modelo.
# - Usamos un dict en memoria (DB) sólo para ejemplos; en producción usarías una BD real.
