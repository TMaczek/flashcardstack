import string
from flashcardstack.models import FlashCard
from django.contrib.auth.models import User
from flashcardstack.helpers.enums import ErrorCode
from datetime import datetime

class DatabaseConnection:

    def __init__(self):
        return

    def addFlashCard(self, _content, _userId, _notice_lvl_id_days=1):
        _user = User.objects.filter(id=_userId).first()
        if _user is None:
            return ErrorCode.ERROR 
        card = FlashCard(user=_user, notice_lvl_in_days=_notice_lvl_id_days, content=_content)
        card.save()
        return ErrorCode.SUCCESS
    
    def getFlashCardCreationDate(self, cardId):
        obj = FlashCard.objects.filter(id=cardId).first()
        if obj is None:
            return None
        return obj.creation_date
    
    def getFlashCardNoticeDate(self, cardId):
        obj = FlashCard.objects.filter(id=cardId).first()
        if obj is None:
            return None
        return obj.date_of_last_notice
    
    def getFlashCardDaysFromLastNotice(self, cardId):
        """returns days from last notice or ErrorCode.ERROR if not found"""
        lastNotice = self.getFlashCardNoticeDate(cardId)
        if lastNotice == None:
            return ErrorCode.ERROR
        dfln = datetime.today().date() - lastNotice
        return dfln.days
    
    def getFlashCardContent(self, cardId):
        obj = FlashCard.objects.filter(id=cardId).first()
        if obj is None:
            return None
        return obj.content
    
    def getFlashCardNoticeLvl(self, cardId):
        obj = FlashCard.objects.filter(id=cardId).first()
        if obj is None:
            return None
        return int(str(obj.notice_lvl_in_days))
    
    def getFlashCardUserId(self, cardId):
        obj = FlashCard.objects.filter(id=cardId).first()
        if obj is None:
            return None
        return obj.user_id
    
    def getUserLastLogin(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.last_login

    def getUserIsSuperuser(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.is_superuser

    def getUserName(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.username

    def getUserFirstName(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.first_name

    def getUserLastName(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.last_name

    def getUserEmail(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.email
        
    def getUserIsStaff(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.is_staff

    def getUserIsActive(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.is_active

    def getUserJoinDate(self, userId):
        obj = User.objects.filter(id=userId).first()
        if obj is None:
            return None
        return obj.date_joined