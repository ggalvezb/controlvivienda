from pymongo import MongoClient

#Base de datos local
#db_client= MongoClient().local

#Base de datos remota
db_client= MongoClient("mongodb+srv://ggalvezb:Serviu2023@cluster0.7k0u5as.mongodb.net/?retryWrites=true&w=majority").desarrollo

