# 🚀 Aprendiendo FastAPI – Proyecto Completo

Este repositorio contiene todos los ejercicios, ejemplos y proyectos desarrollados a lo largo de un curso completo de **FastAPI**, uno de los frameworks más rápidos y modernos para construir APIs con Python.

El objetivo del repositorio es documentar el progreso desde los fundamentos hasta el desarrollo de un sistema de autenticación avanzado con **OAuth2 + JWT**, aplicando conceptos reales utilizados en entornos profesionales.

---

## 📑 Tabla de Contenidos

1. Introducción a FastAPI  
2. Estructura del Proyecto  
3. Instalación y Puesta en Marcha  
4. Módulos y Contenido del Curso  
   - Rutas básicas (GET, POST, PUT, DELETE)  
   - Path y Query Parameters  
   - Manejo de HTTP Status  
   - Routers y modularización  
   - Archivos estáticos  
   - CRUD con Base de Datos simulada  
   - Autenticación con OAuth2 (password flow)  
   - Hashing de contraseñas con Passlib  
   - Generación y validación de JWT  
   - Roles y autorización  
5. Ejercicios y Proyectos incluidos  
6. Licencia  

---

## 📘 1. Introducción a FastAPI

FastAPI es un framework de Python diseñado para crear APIs de manera sencilla y con performance extremadamente alta.  
Se basa en:

- Python moderno (type hints)  
- Pydantic (validación de datos)  
- Starlette (manejo de requests ultrarrápido)  
- Swagger UI integrado  

Este repositorio recopila todos los ejercicios realizados para aprender cada parte del framework de forma progresiva.

---

## 🗂️ 2. Estructura General del Proyecto
Backend/
│
├── Exercises/
│   ├── exercise_01/
│   ├── exercise_02/
│   ├── exercise_03/
│   ├── exercise_04/
│   └── …
│
├── Routers/
│   ├── metodo_get.py
│   ├── metodo_post.py
│   ├── metodo_put.py
│   ├── metodo_delete.py
│   ├── path_query.py
│   ├── http_status.py
│   ├── autorizacion_oauth2.py
│   └── autenticacion_jwt.py
│
├── Static/
│   └── Images/
│
├── main.py
└── README.md

Cada carpeta contiene módulos independientes del curso, permitiendo un aprendizaje progresivo y ordenado.

---

## ⚙️ 3. Instalación y Ejecución

1. Clonar el repositorio:
git clone https://github.com/tunombre/aprendiendo-fastapi.git

2. Crear un entorno virtual:
python3 -m venv venv

3. Activarlo:
source venv/bin/activate   

4. Instalar dependencias generales del curso:
pip install fastapi[standard] passlib[bcrypt] python-jose

5. Ejecutar la API:
fastapi dev main.py

6. Documentación automática disponible en:
http://localhost:8000/docs

---

## 📚 4. Módulos y Contenidos del Curso

### ✓ Rutas y Métodos HTTP
- GET, POST, PUT, DELETE
- Parámetros de ruta
- Validación automática con Pydantic

### ✓ Path y Query Parameters
- Parámetros dinámicos (`/items/1`)
- Parámetros opcionales (`?price_max=100`)

### ✓ Manejo de HTTP Status
- `status_code`
- `HTTPException`
- Errores informativos para cada operación

### ✓ Routers
- Modularización profesional
- Uso de `include_router()`

### ✓ Archivos Estáticos
- Montaje de contenido estático mediante `StaticFiles`

### ✓ CRUD Completo
- Base de datos simulada con listas
- Registro, consulta, modificación y eliminación

### ✓ Autenticación OAuth2 (Password Flow)
- Login con usuario y contraseña
- Tokens tipo Bearer

### ✓ Hashing de Contraseñas (bcrypt)
- Verificación de contraseñas seguras

### ✓ JWT (JSON Web Tokens)
- Generación de tokens con expiración
- Decodificación y validación segura

### ✓ Autorización por Roles
- Permisos para CEO vs empleados
- Rutas protegidas con dependencias

---

## 🧩 5. Ejercicios incluidos

### **Ejercicio 1 – Sistema de Productos**  
CRUD básico con estructura simple y Pydantic.

### **Ejercicio 2 – Gestión de Empleados**  
CRUD completo + manejo profesional de HTTP Status.

### **Ejercicio 3 – Sistema de Usuarios**  
Autenticación con OAuth2, dependencias y roles.

### **Ejercicio 4 – Inventario Autenticado**  
JWT + hashing + permisos + rutas protegidas + CRUD.

---

## 📄 6. Licencia

Este proyecto está disponible bajo la licencia MIT.  
Podés usarlo libremente para estudio y práctica.

---

## ✔️ Listo para usar

Podés clonar, modificar o extender el proyecto para tus propios desarrollos mientras seguís aprendiendo FastAPI.