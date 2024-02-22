from pymongo import MongoClient


#Base de datos local
#db_client= MongoClient().local


#Base de datos remota
db_client= MongoClient('mongodb+srv://test:test1@cluster0.d3zx3lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').test