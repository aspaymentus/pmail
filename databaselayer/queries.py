import pymongo
from .connection import dbConnection

outbox_collection = dbConnection('Pmail' , 'outbox')
inbox_collection = dbConnection('Pmail' , 'inbox')
user_collection = dbConnection('Pmail', 'user_data')

def findQuery(myCollection , findFilter):
    return  myCollection.find_one(findFilter)

def insertQuery(myCollection, payLoad):
    myCollection.insert_one(payLoad)

def findWithProjectionQuery(myCollection , findFilter , projection):
    return myCollection.find_one(findFilter , projection)

def loginQuery(username,status):
    user_collection.update_one({"username" : username},
                            {"$set" : {"is_login" : status}}
                            )

def logoutQuery(status):
    user_collection.update_one({"is_login" : not status},
                            {"$set" : {"is_login" : status}}
                            )

def createCollectionQuery(myCollection,payLoad):
    myCollection.insert_one(payLoad)

def saveEmailQuery(findFilter,payLoad):
    inbox_collection.update_one(findFilter , {"$push" : {"messages" : payLoad}})

def put_message_in_outbox(findFilter,payLoad):
    outbox_collection.update_one(findFilter , {"$push" : {"messages" : payLoad}})

def delete_message_from_outbox(findFilter, message_id):
    outbox_collection.update_one(findFilter , {"$pull" : {"messages" : {"message_id" : message_id}}})



