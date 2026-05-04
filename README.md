# ⚡️ FastAPI 

<p align="center">
  <img 
    src="Imagenes/fastapi.png" 
    width="50%" 
    alt="Descripción de tu imagen"
  />
</p>

En este repositorio vas a encontrar todo el contenido principal para aprender cómo manejar un sistema Backend en FastAPI, uno de los frameworks más rápidos y modernos para construir APIs con Python. El objetivo es documentar el progreso de los fundamentos necesarios para que cualquiera pueda aprender a como construir una base sólida para desarrollar APIs modernas y profesionales. 

```
├── Actividades
│   │
│   ├── exercise_01
│   │   └── tienda.py
│   │
│   ├── exercise_02
│   │   ├── base_model.py
│   │   └── empleados.py
│   │
│   ├── exercise_03
│   │   ├── base_model.py
│   │   └── users_authentication.py
│   │
│   ├── exercise_04
│   │   ├── base_model.py
│   │   └── inventory_managment.py
│   │
│   ├── exercise_05
│   │   ├── base_model.py
│   │   ├── exceptions.py
│   │   └── reservas.py
│   │
│   └── exercise_06
│       ├── base_model.py
│       ├── exceptions.py
│       └── hoteles.py
│
├── Backend
│   │
│   ├── DataBase
│   │   │   
│   │   ├── MongoDB
│   │   │   │
│   │   │   ├── Models
│   │   │   │   └── models.py
│   │   │   ├── Schemas
│   │   │   │   └── schemas.py
│   │   │   └── database.py
│   │   │ 
│   │   └── SQLAlchemy
│   │       │ 
│   │       ├── Models
│   │       │   └── models.py
│   │       ├── Schemas
│   │       │   └── schemas.py
│   │       ├── database.py
│   │       └── sqlalchemy.db
│   │
│   ├── Routers
│   │   │
│   │   ├── autenticacion_jwt.py
│   │   ├── autorizacion_oauth2.py
│   │   ├── creacion_API.py
│   │   ├── exceptions.py
│   │   ├── http_status.py
│   │   ├── llamada_api_externa.py
│   │   ├── metodo_delete.py
│   │   ├── metodo_get.py
│   │   ├── metodo_post.py
│   │   ├── metodo_put.py
│   │   ├── mongoDB.py
│   │   ├── path_query.py
│   │   └── sqlalchemy.py
│   │
│   ├── Static
│   │   │
│   │   └── Images
│   │       ├── image.png
│   │       └── sistemas.png
│   │
│   ├── alembic
│   │   │
│   │   ├── versions
│   │   │   └── 5a198d1d550c_initial_migration.py
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── alembic.ini
│   └── main.py
│   
├── Imagenes
│   ├── fastapi.png
│   └── image.jpg
│   
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

## 📁 Contenido del repositorio

Este curso esta divido en diferentes módulos, de forma de facilitar su lectura y reutilización del código:

- ### 💻 Metodos y Operaciones
El proyecto implementa el ciclo completo CRUD (Create, Read, Update, Delete) siguiendo los estándares de FastAPI. Se trabajó con operaciones `POST`, `GET`, `PUT` y `DELETE`, aplicando validaciones, manejo de errores, modelos Pydantic y respuesta estructurada. Cada operación del sistema respeta las convenciones REST, permitiendo crear recursos, obtener datos de forma individual o listada, actualizar registros existentes y eliminarlos de forma controlada. Esto sienta las bases para construir cualquier tipo de API escalable basada en datos.

- ### ⚙️ Arquitectura del Backend
El proyecto está estructurado de forma modular utilizando `APIRouter`, separando responsabilidad en carpetas como `Backend/`, `DataBase/Models/`, `DataBase/Schemas/` y `Routers/`. Esta arquitectura sigue buenas prácticas profesionales: legibilidad, mantenibilidad y escalabilidad. Cada módulo cumple una función específica dentro del sistema, permitiendo crecer la API sin perder orden.

- ### 🔐 Autenticación y Autorización
Incluye la implementación completa de un sistema seguro basado en JWT, donde se aprendió a generar y validar tokens, manejar expiraciones y controlar el acceso mediante roles y estados del usuario. También se integró OAuth2 con `OAuth2PasswordBearer` y hashing de contraseñas con passlib, aplicando dependencias como `current_user` para proteger rutas y recursos del backend.

- ### 📊 Bases de Datos
Se trabajó con dos enfoques distintos de almacenamiento: MongoDB como base NoSQL y SQLAlchemy para bases SQL relacionales. Con MongoDB se construyó un CRUD completo tanto local como en la nube (Atlas), manejando modelos, esquemas y conversiones con `ObjectId`. Con SQLAlchemy se aprendió a modelar tablas, crear sesiones, definir relaciones básicas y ejecutar operaciones CRUD, entendiendo las diferencias entre los modelos de datos SQL y NoSQL.

- ### 🐳 Docker 
Se creó un entorno completamente dockerizado para ejecutar la API de forma aislada y reproducible. El `Dockerfile` define la construcción de la imagen, instalación de dependencias y arranque de la aplicación. Se generó la imagen, se levantó el contenedor y se expuso el servicio, haciendo posible correr el backend desde cualquier entorno sin configuraciones adicionales.
