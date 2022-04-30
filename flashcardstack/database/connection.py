import pymongo
from django.conf import settings
from flashcardstack.helpers import logger
from flashcardstack.settings import DATABASE_KEY
from datetime import datetime
from flashcardstack.helpers.enums import ErrorCode

class DatabaseConnection:

    def __init__(self):
        connectString = DATABASE_KEY 
        myClient = pymongo.MongoClient(connectString)
        dbname = myClient['flashcardstack']
        self.collectionLogins = dbname["logins"]
        self.collectionFlashcards = dbname["flashcards"]
        self.collectionSubjects = dbname["subjects"]
    
    def __getMaxId(self, collection, idName):
        maxId = collection.find_one(sort=[(idName,-1)]).get(idName,None)
        if maxId == None:
            logger.log("FAULT:: maxId not found")
        return maxId


    def addUser(self, name, login, password):
        """adds user"""
        maxId = self.__getMaxId(self.collectionLogins, "user_id")
        if maxId == None:
            logger.log("FAULT:: user not added")
            return ErrorCode.ERROR
        user = {
            "user_id": maxId + 1,
            "name" : name,
            "login" : login,
            "password" : password
        }
        self.collectionLogins.insert_one(user)
        return ErrorCode.SUCCESS
    
    def __exists(self, collection, field, value):
        login = collection.find_one({field:value})
        if login == None:
            logger.log("FAULT:: %s not found" %field)
            return False
        return True

    def getUserPassword(self, login):
        """returns user password or ErrorCode.Error if not found"""
        if self.__exists(self.collectionLogins, "login", login) == True :
            password = self.collectionLogins.find_one({'login':login}).get("password",None)
            if password == None:
                logger.log("FAULT:: password no found")
                return ErrorCode.ERROR
            return password
        else:
            return ErrorCode.ERROR
    
    def getUserLogin(self, userId):
        """returns user login or ErrorCode.Error if not found"""
        if self.__exists(self.collectionLogins, "user_id", userId) == True :
            login = self.collectionLogins.find_one({'user_id': userId}).get("login",None)
            if login == None:
                logger.log("FAULT:: login no found")
                return ErrorCode.ERROR
            return login
        else:
            return ErrorCode.ERROR
            
    def addFlashcard(self, userId, subjectsId, content):
        """adds flashcard, subjectsId has to be a list"""
        if not isinstance(subjectsId, list):
            logger.log("FAULT:: subjectsId is not an array")
            return ErrorCode.ERROR
        maxId = self.__getMaxId(self.collectionFlashcards, "card_id")
        if maxId == None:
            logger.log("FAULT:: flashcard not added")
            return ErrorCode.ERROR
        flashcard = {
            "card_id" : maxId + 1,
            "userId" : userId,
            "creation_date" : datetime.today().replace(microsecond=0),
            "notice_lvl_in_days" : 1,
            "date_of_last_notice" : datetime.today().replace(microsecond=0),
            "subjectsId" : subjectsId,
            "content" : content
        }
        self.collectionFlashcards.insert_one(flashcard)
        return ErrorCode.SUCCESS

    def getFlashcardCreationDate(self, cardId):
        """returns creation date as datetime or ErrorCode.ERROR if not found"""
        if self.__exists(self.collectionFlashcards, "card_id", cardId) == True:
            creationDate = self.collectionFlashcards.find_one({'card_id': cardId}).get("creation_date",None)
            if creationDate == None:
                logger.log("FAULT:: creation_date not found")
                return ErrorCode.ERROR
            return creationDate
        else:
            return ErrorCode.ERROR
    
    def getFlashcardDaysFromLastNotice(self, cardId):
        """returns days from last notice or ErrorCode.ERROR if not found"""
        if self.__exists(self.collectionFlashcards, "card_id", cardId) == True:
            lastNotice = self.collectionFlashcards.find_one({'card_id': cardId}).get("date_of_last_notice",None)
            if lastNotice == None:
                logger.log("FAULT:: date of last notice not found")
                return ErrorCode.ERROR
            dfln = datetime.today().replace(microsecond=0) - lastNotice
            return dfln.days
        else:
            return ErrorCode.ERROR

    def FlashcardChangeNoticeLvl(self, cardId, newNoticeLvl):
        """changes notice level in days"""
        if self.__exists(self.collectionFlashcards, "card_id", cardId) == True:
            result = self.collectionFlashcards.update_one({'card_id': cardId}, {'$set':{'notice_lvl_in_days':newNoticeLvl}})
            if result.matched_count > 0:
                return ErrorCode.SUCCESS
            else:
                return ErrorCode.ERROR
        else:
            return ErrorCode.ERROR
    
    def addSubject(self, userId, subjectName, description):
        """adds subject"""
        maxId = self.__getMaxId(self.collectionSubjects, "subject_id")
        if maxId == None:
            logger.log("FAULT:: subject not added")
            return ErrorCode.ERROR
        subject = {
            "subject_id" : maxId + 1,
            "userId" : userId,
            "subject_name" : subjectName,
            "description" : description
        }
        self.collectionSubjects.insert_one(subject)
        return ErrorCode.SUCCESS
    
    def getSubjectName(self, subjectId):
        """returns name of subject or ErrorCode.ERROR if not found"""
        if self.__exists(self.collectionSubjects, "subject_id", subjectId) == True:
            subjectName = self.collectionSubjects.find_one({"subject_id": subjectId}).get("subject_name", None)
            if subjectName == None:
                logger.log("FAULT:: subjectName not found")
                return ErrorCode.ERROR
            return subjectName
        else:
            return ErrorCode.ERROR