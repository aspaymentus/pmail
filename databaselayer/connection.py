import pymongo
from pymongo import MongoClient
import json

def dbConnection(dbName , collectionName):
    with open("databaselayer\config.json") as file:
        data = json.load(file)
    myClient = MongoClient(data['dbHost'])
    myDb = myClient[dbName]
    myCollection = myDb[collectionName]
    return myCollection
