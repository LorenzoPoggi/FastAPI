"""
dashboard_simple.py

Dashboard ejemplo 1 — "Simple".

Objetivo: mostrar una página GET que contiene enlaces y botones para
 - navegar (GET)
 - abrir un formulario que hace POST (multipart upload)
 - hacer un POST con fetch (AJAX)

Explicación: cada bloque tiene comentarios en español que explican línea a línea
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse

# Creamos la aplicación FastAPI
app = FastAPI()


@app.get("/simple/dashboard", response_class=HTMLResponse)
async def simple_dashboard():
    """Ruta GET que devuelve el HTML del dashboard.

    Esta ruta se usa sólo para mostrar la interfaz (es una vista simple).
    Desde aquí el usuario puede navegar o activar acciones que llamen a
    endpoints POST.
    """
    # HTML minimalista con enlaces y botones
    html = """
    <html>
      <head><meta charset='utf-8'/><title>Dashboard Simple</title></head>
      <body>
        <h1>Dashboard Simple</h1>
        <p><a href="/simple/page">Ir a una página (GET)</a></p>

        <p><a href="/simple/upload_form">Abrir formulario de subida (POST)</a></p>

        <p>
          <button id="btnFetch">Enviar POST (fetch) a /simple/api/do</button>
        </p>
        <pre id="result"></pre>

        <script>
        document.getElementById('btnFetch').addEventListener('click', async ()=>{
          // Ejemplo de POST usando fetch y JSON
          const payload = { action: 'ping', when: Date.now() };
          const res = await fetch('/simple/api/do', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const data = await res.json();
          document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        });
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/simple/page", response_class=HTMLResponse)
async def simple_page():
    """Página de destino a la que se navega vía GET (enlace simple)."""
    return HTMLResponse("""
      <html>
        <body>
          <h2>Página simple (GET)</h2>
          <p>Esta página confirma que la navegación GET funciona.</p>
          <p><a href="/simple/dashboard">Volver al dashboard</a></p>
        </body>
      </html>
    """)


@app.get("/simple/upload_form", response_class=HTMLResponse)
async def simple_upload_form():
    """Formulario HTML que envía un multipart POST a /simple/upload."""
    html = """
    <html>
      <body>
        <h2>Formulario de subida</h2>
        <form action="/simple/upload" enctype="multipart/form-data" method="post">
          <input type="file" name="file" />
          <button type="submit">Subir archivo</button>
        </form>
        <p><a href="/simple/dashboard">Volver</a></p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post("/simple/upload")
async def simple_upload(file: UploadFile = File(...)):
    """Endpoint que recibe el archivo enviado por el formulario.

    - `UploadFile` es la forma recomendada en FastAPI para manejar ficheros.
    - Aquí leemos el contenido y devolvemos metadata simple.
    """
    content = await file.read()
    return JSONResponse({
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content)
    })


@app.post("/simple/api/do")
async def simple_api_do(payload: dict):
    """Endpoint JSON que recibe un POST desde fetch y responde con JSON."""
    # Payload ya llega como dict si el cliente envía JSON y Content-Type correcto
    return JSONResponse({"ok": True, "echo": payload})
