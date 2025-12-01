# llamada_api_externa.py 

from fastapi import APIRouter, HTTPException
from typing import Optional
import os
from pydantic import BaseModel
import httpx 
from tenacity import retry, stop_after_attempt, wait_exponential # libreria de reintentos

router = APIRouter(tags=["Weather API client example"])

# -------------------------------------------
# Configuracion que lee variables de entorno
# -------------------------------------------

# Esta clase sirve para gestionar configuraciones
class Settings(BaseModel):
    OPENWEATHER_API_KEY: Optional[str] = None
    # Configuración para leer desde .env si es necesario
    class Config:
        # Lee variables desde .env si existe
        env_file = ".env"  
# Instancia de configuración 
settings = Settings()

# --------------------------
# Cliente HTTP asincrónico
# --------------------------

# Creamos una única instancia de AsyncClient que reutilizaremos
http_client = httpx.AsyncClient(timeout=10.0)

# Decorador de reintentos: intenta hasta 3 veces con backoff exponencial
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
# Función para hacer peticiones GET y devolera la informacion en JSON
async def fetch_json(url: str, params: dict = None) -> dict:
    # Peticion HTTP GET a la URl con parametros dados
    response = await http_client.get(url, params=params)
    response.raise_for_status()  
    # Devuelve el contenido JSON de la respuesta
    return response.json()

# ---------------------------------
# Operaciones del sistema backend 
# ---------------------------------

# Operacion para obtener el clima de una ciudad
@router.get("/weather")
async def get_weather(city: str):
    # Leemos la API key desde configuracion o variable de entorno
    api_key = settings.OPENWEATHER_API_KEY or os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        # Si no hay API key configurada, devolvemos error 500 con mensaje claro
        raise HTTPException(status_code=500, detail="OPENWEATHER_API_KEY no configurada")

    # Definimos la URL y los parametros para la llamada a la API externa
    url = "https://api.openweathermap.org/data/2.5/weather"
    # Parametros de consulta
    params = {"query": city, "appid": api_key, "units": "metric"}  # units=metric devuelve °C

    # Hacemos la llamada a la API externa con manejo de errores
    try:
        # Llamada real a la API externa
        data = await fetch_json(url, params=params)  
    except httpx.HTTPStatusError as e:
        # Si la API respondió 4xx/5xx, devolvemos el código y un mensaje legible
        raise HTTPException(status_code=e.response.status_code, detail="Error desde OpenWeather")
    except httpx.RequestError:
        # Errores de conexión / timeout
        raise HTTPException(status_code=502, detail="Fallo de conexión a OpenWeather")
    except Exception:
        # Cualquier otro error no esperado
        raise HTTPException(status_code=500, detail="Error interno")

    # Devolvemos algunos datos útiles (podés adaptar la estructura)
    return {
        "city": city,
        "temperature": data.get("main", {}).get("temp"),
        "description": data.get("weather", [{}])[0].get("description"),
        "raw": data  # opcional: puedes quitar esto si no querés exponer todo
    }