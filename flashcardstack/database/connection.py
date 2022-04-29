import pymongo
from django.conf import settings
from flashcardstack.helpers import logger

class DatabaseConnection:

    def __init__(self):
        connectString = 'mongodb+srv://flashcardstack:flashcardstack@cluster0.v42ws.mongodb.net/project0?retryWrites=true&w=majority' 
        myClient = pymongo.MongoClient(connectString)
        dbname = myClient['flashcardstack']
        self.collectionLogins = dbname["logins"]

    def insertUser(self, name, login, password):
        maxId = self.collectionLogins.find_one(sort=[("user_id",-1)]).get("user_id",None)
        if maxId == None:
            logger.log("FAULT:: maxId not found, user not added")
            return
        addUser = {
            "user_id": maxId + 1,
            "name" : name,
            "login" : login,
            "password" : password
        }
        self.collectionLogins.insert_one(addUser)
    
    def existsInLogins(self, field, value):
        login = self.collectionLogins.find_one({field:value})
        if login == None:
            logger.log("FAULT:: %s not found" %field)
            return False
        return True

    def getUserPassword(self, login):
        if self.existsInLogins("login",login) == True :
            password = self.collectionLogins.find_one({'login':login}).get("password",None)
            if password == None:
                logger.log("FAULT:: password no found")
                return None
            return password
        else:
            return None
