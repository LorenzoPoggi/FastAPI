# Imagen base oficial de Python
FROM python:3.12-slim

# Creacion del directorio de trabajo dentro del contenedor
WORKDIR /app

# Copio los archivos del proyecto
COPY . /app

# Instalacion de dependencias 
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el contenedor
EXPOSE 8000

# Comando para lanzar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
