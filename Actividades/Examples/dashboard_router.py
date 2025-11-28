"""
dashboard_router.py

Dashboard ejemplo 3 — Uso de APIRouter y organización similar a tus `Routers/`.

Objetivo: mostrar cómo crear un `APIRouter`, agrupar rutas relacionadas
y luego `include_router` desde `main.py`. Esto es lo que estás aprendiendo
en el curso con la carpeta `Routers/`.
"""

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

# Creamos un router en lugar de app.
router = APIRouter(prefix="/router", tags=["RouterDashboard"]) 


@router.get('/dashboard', response_class=HTMLResponse)
async def router_dashboard():
    """Dashboard servido por un router. Esto facilita incluirlo en `main.py`.

    - Todas las rutas definidas aquí quedan bajo `/router` por el `prefix`.
    - Desde `main.py` harías `app.include_router(router)` para registrarlo.
    """
    html = """
    <html>
      <head><meta charset='utf-8'/><title>Router Dashboard</title></head>
      <body>
        <h1>Router Dashboard</h1>
        <p>GET simple: <a href="/router/info">/router/info</a></p>
        <p>POST via fetch a <code>/router/action</code> (desde JS)</p>
        <script>
          async function run(){
            const res = await fetch('/router/action', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({msg:'hello'})});
            const j = await res.json();
            console.log(j);
          }
          run();
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@router.get('/info')
async def router_info():
    """Ruta GET simple que devuelve información JSON."""
    return JSONResponse({"info": "Este es un router separado (prefix /router)"})


@router.post('/action')
async def router_action(payload: dict):
    """Ejemplo de acción POST dentro del router."""
    # Procesa payload y devuelve respuesta
    return JSONResponse({"received": payload, "ok": True})


# Pequeña nota para integrar en `main.py`:
# - En `main.py` importar: `from Examples.dashboard_router import router as dashboard_router`
# - Y luego: `app.include_router(dashboard_router)` o con prefix/ tags adicionales.

# Si prefieres montar todo como app separada: `app.mount('/examples', router_app)`
