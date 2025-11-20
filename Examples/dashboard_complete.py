"""
dashboard_complete.py

Dashboard completo — archivo de referencia "todo en uno" para aprender FastAPI.

Características incluidas:
- API REST CRUD para un recurso `Item` (usando Pydantic `BaseModel`).
- Paginación, búsqueda y filtrado simples.
- Subida y guardado de archivos en carpeta `uploads/`.
- Endpoints protegidos por una dependencia de autenticación simple (mock).
- Interfaz HTML interactiva (GET) que usa fetch para llamar a los endpoints (POST/PUT/DELETE).
- El archivo exporta tanto `router` como `app` para poder `include_router(...)` o ejecutar directamente.

Instrucciones rápidas:
- Ejecutar con `fastapi dev Examples/dashboard_complete.py` (si dispones de `fastapi dev`).
- Alternativa con uvicorn:
    uvicorn Examples.dashboard_complete:app --reload --port 8003

Este archivo está comentado en español para facilitar el aprendizaje.
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import os
import uuid

# -----------------------
# Configuración básica
# -----------------------

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)  # crear carpeta uploads si no existe

# Creamos router y app. Exportamos ambos para flexibilidad.
router = APIRouter(prefix="/complete", tags=["CompleteDashboard"])  # similar a tus Routers/
app = FastAPI(title="Dashboard Complete Example")
app.include_router(router)


# -----------------------
# Modelos Pydantic
# -----------------------

class ItemBase(BaseModel):
    # Campos que el cliente puede enviar al crear/actualizar
    name: str = Field(..., example="Mi item")
    description: Optional[str] = Field(None, example="Descripción opcional")
    price: float = Field(..., gt=0, example=9.99)


class ItemCreate(ItemBase):
    # Por claridad, separamos el esquema de creación
    pass


class ItemUpdate(BaseModel):
    # Todos los campos opcionales para actualización parcial
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ItemOut(ItemBase):
    # Esquema de salida que incluye id y timestamps
    id: str
    created_at: datetime


# -----------------------
# Dependencia de autenticación (mock)
# -----------------------

def get_current_user(request: Request):
    """Dependencia simple para simular autenticación.

    - Busca header `Authorization: Bearer <token>` o `X-User`.
    - En este ejemplo, si el token es 'admin' se considera usuario con role 'admin'.
    - Esto permite proteger rutas con `Depends(get_current_user)`.
    """
    auth = request.headers.get('authorization') or request.headers.get('x-user')
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No autenticado')
    # soportar 'Bearer token' o solo token
    token = auth.split()[-1]
    # mock simple: 'admin' tiene permisos, cualquier otro token es usuario normal
    if token == 'admin':
        return {"username": "admin", "role": "admin"}
    return {"username": token, "role": "user"}


# -----------------------
# "Base de datos" en memoria
# -----------------------

# Usamos un dict simple {id: item_dict} para el ejemplo. En producción usar DB real.
DB: Dict[str, Dict] = {}


def _generate_id() -> str:
    return str(uuid.uuid4())


# -----------------------
# CRUD API
# -----------------------

@router.post('/items', response_model=ItemOut)
async def create_item(item: ItemCreate, user: dict = Depends(get_current_user)):
    """Crear un item (POST /complete/items).

    - `item` será validado automáticamente contra `ItemCreate`.
    - Requiere autenticación (Dependencia).
    """
    item_id = _generate_id()
    now = datetime.utcnow()
    stored = item.model_dump()  # Pydantic v2
    stored.update({"id": item_id, "created_at": now})
    DB[item_id] = stored
    # Devolver el dict directamente permite que FastAPI aplique el
    # `response_model` y serialice tipos como `datetime` correctamente.
    return stored


@router.get('/items', response_model=List[ItemOut])
async def list_items(q: Optional[str] = None, skip: int = 0, limit: int = 20):
    """Listar items con paginación y búsqueda simple por nombre.

    - `q`: término de búsqueda (filtro por `name` contiene q)
    - `skip` y `limit` para paginar resultados
    """
    items = list(DB.values())
    if q:
        items = [it for it in items if q.lower() in it['name'].lower()]
    # ordenar por created_at (reciente primero)
    items.sort(key=lambda x: x['created_at'], reverse=True)
    return items[skip: skip + limit]


@router.get('/items/{item_id}', response_model=ItemOut)
async def get_item(item_id: str):
    """Obtener un item por id."""
    if item_id not in DB:
        raise HTTPException(status_code=404, detail='Item no encontrado')
    return DB[item_id]


@router.put('/items/{item_id}', response_model=ItemOut)
async def update_item(item_id: str, item: ItemUpdate, user: dict = Depends(get_current_user)):
    """Actualizar un item (PUT). Campos opcionales."""
    if item_id not in DB:
        raise HTTPException(status_code=404, detail='Item no encontrado')
    stored = DB[item_id]
    update_data = item.model_dump(exclude_unset=True)
    stored.update(update_data)
    DB[item_id] = stored
    return stored


@router.delete('/items/{item_id}')
async def delete_item(item_id: str, user: dict = Depends(get_current_user)):
    """Eliminar item. Solo admin puede eliminar en este ejemplo."""
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Permiso denegado')
    if item_id not in DB:
        raise HTTPException(status_code=404, detail='Item no encontrado')
    del DB[item_id]
    return JSONResponse({"deleted": True, "id": item_id})


# -----------------------
# Upload: recibir y guardar archivos
# -----------------------

@router.post('/upload')
async def upload_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    """Recibe un archivo y lo guarda en la carpeta `uploads/`.

    - Devuelve la ruta relativa donde quedó guardado.
    """
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    # Leer y escribir chunk a chunk para no agotar memoria con ficheros grandes
    with open(path, 'wb') as f:
        content = await file.read()
        f.write(content)
    return JSONResponse({"filename": filename, "path": path})


# -----------------------
# Search endpoint (ejemplo POST para búsquedas avanzadas)
# -----------------------

@router.post('/search')
async def search_items(term: str = Form(...)):
    """Formulario simple que busca por nombre (ejemplo de uso de Form data).

    - Muestra que puedes aceptar `Form` en lugar de JSON si el cliente envía datos de formulario.
    """
    found = [it for it in DB.values() if term.lower() in it['name'].lower()]
    return JSONResponse({"count": len(found), "results": found})


# -----------------------
# Endpoint que devuelve la interfaz HTML del dashboard
# -----------------------

@router.get('/dashboard', response_class=HTMLResponse)
async def complete_dashboard():
    """Interfaz HTML que demuestra las operaciones principales.

    - Usa fetch para llamar a los endpoints: crear, listar, eliminar, upload.
    - Muestra cómo enviar encabezado `Authorization: Bearer admin` para acciones protegidas.
    """
    html = """
    <html>
      <head><meta charset='utf-8'/><title>Dashboard Complete</title></head>
      <body>
        <h1>Dashboard Complete</h1>

        <section>
          <h2>Crear Item (POST JSON)</h2>
          <p>Nombre: <input id='name'/></p>
          <p>Precio: <input id='price' type='number' step='0.01'/></p>
          <button id='create'>Crear (requiere auth)</button>
        </section>

        <section>
          <h2>Listar Items (GET)</h2>
          <p>Buscar: <input id='q'/> <button id='search'>Buscar</button></p>
          <div id='items'></div>
        </section>

        <section>
          <h2>Subir archivo (multipart/form-data)</h2>
          <form id='uploadForm' enctype='multipart/form-data'>
            <input type='file' name='file' id='file' />
            <button type='submit'>Subir (requiere auth)</button>
          </form>
          <div id='uploadResult'></div>
        </section>

        <section>
          <h2>Notas sobre autenticación en este ejemplo</h2>
          <p>Para llamadas protegidas añade header <code>Authorization: Bearer admin</code> (admin) o cualquier otro token (user).</p>
        </section>

        <script>
          const authHeader = {'Authorization': 'Bearer admin'}; // cambiar a otro token para role user

          async function refresh(q){
            const url = q ? `/complete/items?q=${encodeURIComponent(q)}` : '/complete/items';
            const res = await fetch(url);
            const items = await res.json();
            const container = document.getElementById('items');
            container.innerHTML = JSON.stringify(items, null, 2);
          }

          document.getElementById('create').addEventListener('click', async ()=>{
            const name = document.getElementById('name').value || 'sin-nombre';
            const price = parseFloat(document.getElementById('price').value || '1');
            const payload = {name, price};
            const res = await fetch('/complete/items', {method:'POST', headers:{'Content-Type':'application/json', ...authHeader}, body: JSON.stringify(payload)});
            const j = await res.json();
            console.log('created', j);
            await refresh();
          });

          document.getElementById('search').addEventListener('click', async ()=>{
            const q = document.getElementById('q').value;
            await refresh(q);
          });

          document.getElementById('uploadForm').addEventListener('submit', async (e)=>{
            e.preventDefault();
            const fileEl = document.getElementById('file');
            if(!fileEl.files.length) return alert('Elige un archivo');
            const fd = new FormData();
            fd.append('file', fileEl.files[0]);
            const res = await fetch('/complete/upload', {method:'POST', headers: {'Authorization': 'Bearer admin'}, body: fd});
            const j = await res.json();
            document.getElementById('uploadResult').textContent = JSON.stringify(j, null, 2);
          });

          // refrescar al cargar
          refresh();
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


# -----------------------
# Notas y explicaciones (resumen)
# -----------------------
# - FastAPI valida automáticamente los cuerpos JSON contra los modelos Pydantic.
# - `Depends(get_current_user)` aplica la dependencia de autenticación.
# - `UploadFile` permite manejar archivos en multipart/form-data de manera eficiente.
# - Para pruebas locales, puedes usar `Authorization: Bearer admin` en headers
#   para simular un usuario admin y poder eliminar o subir archivos.
# - `app` está expuesto para ejecución directa: `uvicorn Examples.dashboard_complete:app`.
