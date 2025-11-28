# database.py
from pymongo import MongoClient

# Variable del cliente que se conecta a la base de datos local de MongoDB
db_client = MongoClient("mongodb://localhost:27017/")