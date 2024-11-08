from pymongo import MongoClient
from dotenv import dotenv_values
config = dotenv_values(".env")

mongo_client = None

def get_mongo_client():
    if (mongo_client == None):
        db_user = config['MONGO_INITDB_ROOT_USERNAME']
        db_pass = config['MONGO_INITDB_ROOT_PASSWORD']
        uri = f'mongodb://{db_user}:{db_pass}@mongodb:27017'
        mongo_client = MongoClient(uri)

    return mongo_client

def get_collection(name):
    return get_mongo_client().database[name]