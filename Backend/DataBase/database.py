# database.py
from pymongo import MongoClient

# Variable del cliente que se conecta a la base de datos local de MongoDB
db_client = MongoClient("mongodb://localhost:27017/")

# ----------------------------------------------------
# Comandos para manejar la base de datos MongoDB
# ----------------------------------------------------

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