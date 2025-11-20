# ⚡️ FastAPI – Curso de Backend

En este repositorio vas a encontrar todo el contenido principal para aprender cómo manejar un sistema Backend en uno de los frameworks más rápidos y modernos para construir APIs con Python. También incluye ejercicios, ejemplos y proyectos desarrollados a lo largo del curso.

Este repositorio tiene el fin de documentar todo el progreso de los fundamentos necesarios para el desarrollo de un sistema de autenticación avanzado, aplicando conceptos reales usados en entornos profesionales.

---

## Tabla de Contenidos

1. [Introducción a FastAPI](#-1-introducción-a-fastapi)  
2. [Estructura del Proyecto](#️-2-estructura-general-del-proyecto)  
3. [Instalación y Dependencias](#️-3-instalación-y-ejecución)  
4. [Módulos y Contenido del Curso](#-4-módulos-y-contenidos-del-curso)  
5. [Ejercicios y Proyectos Incluidos](#-5-ejercicios-incluidos)  
6. [Licencia](#-6-licencia)

---

## 1. Introducción a FastAPI

FastAPI es un framework de Python diseñado para crear APIs de manera sencilla y con performance alta.  
Se basa en:

- Python moderno (type hints)  
- Pydantic (modelado de datos)  
- Starlette (manejo de requests ultrarrápido)  
- Swagger UI integrado  

Este repositorio recopila ejercicios realizados para aprender cada parte del framework de forma progresiva.

---

## 2. Estructura General del Proyecto

```txt
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
```

Cada carpeta contiene módulos independientes del curso, permitiendo un aprendizaje progresivo y ordenado.

---

## 3. Instalación y Ejecución

1. Clonar el repositorio:
```txt
git clone https://github.com/LorenzoPoggi/FastAPI-Backend
```

2. Crear un entorno virtual:
```txt
python3 -m venv venv
```

3. Activarlo:
```txt
source venv/bin/activate   
```

4. Instalar dependencias generales del curso:
```txt
pip install fastapi[standard] passlib[bcrypt] python-jose
```

5. Ejecutar la API:
```txt
fastapi dev main.py
```

6. Documentación automática disponible en:
```txt
http://localhost:8000/docs
```

---

## 4. Módulos y Contenidos del Curso

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

Este proyecto está disponible bajo la Licencia MIT.  

---

## ✔️ Listo para usar

Podés clonar, modificar o extender el proyecto para tus propios desarrollos mientras seguís aprendiendo FastAPI.