# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Routers.metodo_get import router as router_get
from Routers.metodo_post import router as router_post
from Routers.metodo_put import router as router_put
from Routers.metodo_delete import router as router_delete
from Routers.path_query import router as router_path_query
from Routers.http_status import router as router_http_status
from Routers.autorizacion_oauth2 import router as router_oauth2
from Routers.autenticacion_jwt import router as router_jwt

app = FastAPI()

# Incluimos las rutas de cada módulo
app.include_router(router_get)
app.include_router(router_post)
app.include_router(router_put)
app.include_router(router_delete)
app.include_router(router_path_query)
app.include_router(router_http_status)
app.mount('/Static', StaticFiles(directory= 'Static/Images/'), name= 'Frontend_Backend')
app.mount('/Static', StaticFiles(directory= 'Static/Images/'), name= 'Sistemas')
app.include_router(router_oauth2)
app.include_router(router_jwt)