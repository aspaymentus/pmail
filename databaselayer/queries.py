import pymongo

def findQuery(myCollection , findFilter):
    return  myCollection.find_one(findFilter)

def insertQuery(myCollection, payLoad):
    myCollection.insert_one(payLoad)

def findWithProjectionQuery(myCollection , findFilter , Projection):
    return myCollection.find_one(findFilter , Projection)

def loginQuery(myCollection,username,status):
    myCollection.update_one({"username" : username},
                            {"$set" : {"is_login" : status}}
                            )

def logoutQuery(myCollection,status):
    myCollection.update_one({"is_login" : not status},
                            {"$set" : {"is_login" : status}}
                            )

def createInboxQuery(myCollection,payLoad):
    myCollection.insert_one(payLoad)

def saveEmailQuery(myCollection,findFilter,payLoad):
    myCollection.update_one(findFilter , {"$push" : {"messages" : payLoad}})



