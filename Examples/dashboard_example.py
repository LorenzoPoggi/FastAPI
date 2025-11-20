"""
dashboard_example.py

Ejemplos para aprender cómo combinar GET y POST en FastAPI desde un "dashboard".

Incluye:
- Secciones separadas explicadas: GET, POST, redirect, misma ruta GET+POST
- Un "Dashboard" (GET) con botones que: navegan a otra página, abren un formulario de subida (POST), lanzan un POST vía fetch (AJAX), y muestran cómo forzar un POST cliente-side.
- Una sección integrada que combina todo.

Instrucciones de uso:
1) Ejecutar: `uvicorn Examples/dashboard_example:app --reload --port 8001`
2) Abrir `http://localhost:8001/dashboard`

"""

from fastapi import FastAPI, Request, UploadFile, File, Form, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Optional

app = FastAPI(title="Dashboard Examples")


# -------------------------
# 1) Ejemplo: Rutas separadas (GET y POST) para la misma ruta
# -------------------------

@app.get("/resource", response_class=JSONResponse)
async def resource_get():
    return {"method": "GET", "message": "Esta es la ruta GET /resource"}


@app.post("/resource", response_class=JSONResponse)
async def resource_post(payload: dict | None = None):
    return {"method": "POST", "message": "Esta es la ruta POST /resource", "payload": payload}


# -------------------------
# 2) Ejemplo: Un mismo handler acepta GET y POST
# -------------------------

@app.api_route("/both", methods=["GET", "POST"])
async def both(request: Request):
    if request.method == "GET":
        return {"method": "GET", "note": "Mismo endpoint acepta GET"}
    data = await request.json() if request.headers.get("content-type", "").startswith("application/json") else None
    return {"method": "POST", "received": data}


# -------------------------
# 3) Upload: formulario (GET) + handler POST para fichero
# -------------------------

@app.get("/upload_form", response_class=HTMLResponse)
async def upload_form():
    # Formulario que sube archivos via POST a /upload
    html = """
    <html>
      <head><title>Upload Form</title></head>
      <body>
        <h2>Subir archivo (POST a /upload)</h2>
        <form action="/upload" enctype="multipart/form-data" method="post">
          <input name="file" type="file" />
          <button type="submit">Subir</button>
        </form>
        <p><a href="/dashboard">Volver al Dashboard</a></p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # No guardamos en disco en este ejemplo; solo leemos un pedazo y devolvemos info
    content = await file.read()
    size = len(content)
    return {"filename": file.filename, "content_type": file.content_type, "size_bytes": size}


# -------------------------
# 4) AJAX / Fetch: endpoint que recibe JSON desde frontend
# -------------------------

@app.post("/api/do_action")
async def do_action(payload: dict):
    # Simula procesamiento de una acción desde el dashboard usando fetch/axios
    # Devuelve resultado JSON
    return {"status": "ok", "received": payload}


# -------------------------
# 5) Redirects y cómo "forzar" un POST desde una navegación
# -------------------------

@app.get("/page", response_class=HTMLResponse)
async def page():
    return HTMLResponse("""
    <html>
      <body>
        <h1>Página de destino (GET)</h1>
        <p>Esta es una página a la que se puede redirigir con GET.</p>
        <p><a href="/dashboard">Volver al Dashboard</a></p>
      </body>
    </html>
    """)


@app.get("/redirect-to-page")
async def redirect_to_page():
    # Redirección BAJA (GET) — no cambia el método del cliente.
    return RedirectResponse(url="/page", status_code=status.HTTP_302_FOUND)


@app.get("/goto-post", response_class=HTMLResponse)
async def goto_post_form():
    # Si necesitas que una navegación (click) termine en una petición POST,
    # el servidor puede responder con HTML que contenga un form y un script
    # que lo auto-envíe (cliente realiza el POST).
    html = """
    <html>
      <body>
        <h3>Ahora se realizará un POST automático a /resource</h3>
        <form id="autoForm" action="/resource" method="post">
          <input type="hidden" name="from" value="goto-post" />
        </form>
        <script>document.getElementById('autoForm').submit();</script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


# -------------------------
# 6) Dashboard integrado (GET) — contiene: link GET, formulario POST, AJAX POST, redirect-to-post
# -------------------------

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    # Página principal (GET) que muestra controles para diversas interacciones
    html = """
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Dashboard - Ejemplos FastAPI</title>
      </head>
      <body>
        <h1>Dashboard de ejemplo</h1>

        <section>
          <h2>1) Navegar a otra página (GET)</h2>
          <p><a href="/page">Ir a /page (GET)</a></p>
        </section>

        <section>
          <h2>2) Abrir formulario de subida (POST)</h2>
          <p><a href="/upload_form">Abrir formulario de subida</a></p>
        </section>

        <section>
          <h2>3) Hacer POST via fetch (AJAX)</h2>
          <button id="btnFetch">Enviar POST (fetch) a /api/do_action</button>
          <pre id="fetchResult"></pre>
        </section>

        <section>
          <h2>4) Redirigir a una acción POST (cliente auto-submit)</h2>
          <p><a href="/goto-post">Ir a /goto-post (esto hará un POST tras cargar la página)</a></p>
        </section>

        <section>
          <h2>5) Ejemplos en la misma ruta</h2>
          <p>GET /resource: <a href="/resource">probar GET</a></p>
          <p>POST /resource: se puede hacer desde un cliente o desde la sección AJAX</p>
        </section>

        <script>
          document.getElementById('btnFetch').addEventListener('click', async function(){
            const payload = { action: 'test', timestamp: Date.now() };
            const res = await fetch('/api/do_action', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });
            const data = await res.json();
            document.getElementById('fetchResult').textContent = JSON.stringify(data, null, 2);
          });
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


# -------------------------
# NOTAS (en español)
# -------------------------
# - Si quieres que un enlace (click) en el dashboard haga una POST, debes
#   usar un formulario con method="post" (o usar JS fetch/axios para hacer
#   la petición desde el cliente). Un redirect 3xx desde el servidor no
#   convertirá un GET en POST: los navegadores no cambian método salvo casos
#   especiales (307/308 mantienen el método original).
# - Recomendación práctica: para acciones que no sean idempotentes (crear,
#   subir ficheros, modificar recursos) usa POST desde el cliente (form o
#   fetch). Para cargar vistas y recursos usa GET.
# - Para integrar en tu app existente (`main.py`) puedes incluir este router
#   o simplemente importar `dashboard_example.app` como aplicación independiente
#   o montar sus rutas. Ejemplo simple en `main.py`:
#     from dashboard_example import app as dashboard_app
#     main_app.mount('/examples', dashboard_app)
#   Sin embargo, si quieres que todo esté en un solo FastAPI, convierte las
#   rutas de este archivo en un `APIRouter` y `include_router(...)`.
