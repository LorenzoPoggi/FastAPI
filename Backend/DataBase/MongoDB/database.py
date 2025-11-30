# database.py
from pymongo import MongoClient

# ------------------------------------------------------
# Comandos para manejar la base de datos MongoDB LOCAL
# ------------------------------------------------------

# Variable del cliente que se conecta a la base de datos local de MongoDB
db_client = MongoClient("mongodb://localhost:27017/").local # Prefijo local

# Comando para iniciar el servidor de MongoDB
# /Users/lorenzo.poggi/Downloads/mongodb-macos-aarch64--8.2.2/bin/mongod --config /usr/local/etc/mongod.conf &

# Comando para conectarse a la base de datos MongoDB
# /opt/homebrew/bin/mongosh

# Comandos para eliminar carpetas de la base de datos 
# use local -> db.*carpeta_a_eliminar*.drop()

# Comando para finalizar mi base de datos
# db.adminCommand("shutdown")

# Comando para conectarse a la base de datos desde Visual Studio
# mongodb://localhost:27017

# ------------------------------------------------------
# Guia para manejar la base de datos MongoDB en la NUBE
# ------------------------------------------------------

# Variable para conectarme a una base de datos que esta en la nube 
db_client_atlas = MongoClient("mongodb://url-proporcionada-de-mongodb-atlas").prefijo

'''
Creo el Proyecto en el cual va a estar mi base de datos desde MongoDB Atlas.
Luego creo el Cluter (DataBase) con el user y la password correspondiente. 
Obtengo la IP de la Base de Datos y configuro quien puede acceder a esta. 
En "Connect" me da la informacion de como conectarme, todo la opcion de VS Code y
me dara el paso a paso para conectarme. 
Desde la extension de VS Code pongo la URL de la base de datos y me conecto. 
Opero de misma forma como si fuera local
'''