from .db import db
import hashlib
from flask_login import UserMixin


class UserModel(UserMixin):

    @staticmethod
    def add_user(username, password):
        hashedPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
        db.store(username, hashedPassword)

    @staticmethod
    def is_exsit(username):
        return True if db.searchExistUser(username) == 1 else False

    @staticmethod
    def checkPassword(username, password):
        passworrd_db = db.searchPassword(username)
        hashedPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if passworrd_db == hashedPassword:
            return True
        else:
            return False

    @staticmethod
    def add_room(username, room_id):
        db.storeRoom(username, room_id)

    @staticmethod
    def allrooms(username):
        roomList = db.searchRoom(username)
        return roomList

    @staticmethod
    def add_record(messageData):
        room = messageData["room"]
        message = messageData["message"]
        fromWho = messageData["from"]
        time = messageData["datetime"]
        print(type(time))
        db.storeRecord(room=room, message=message, fromWho=fromWho, time=time)

    @staticmethod
    def searchUserinfo(searchUsername):
        return db.searchUser(searchUsername)

    @staticmethod
    def add_invitation(invitation):
        db.storeInvitation(fromWho=invitation["from"], toWho=invitation["to"])

    @staticmethod
    def sendInvitation(toWho,fromWho):
        return db.searchInvitation(toWho,fromWho)
    
    @staticmethod
    def delInvitation(invitation):
        fromWho=invitation["from"]
        toWho=invitation["to"]
        db.delInvitation(fromWho=fromWho,toWho=toWho)

    @staticmethod
    def allfriendInvitation(username):
        return list(map(lambda x:x[0], db.searchFriendInvitation(username)))

    #返回newfriend的房號
    @staticmethod
    def add_friend(user_1,user_2):
        return db.storeFriend(user_1,user_2)

    @staticmethod
    def is_invitationExist(fromWho,toWho):
        return True if db.searchExistInvitation(fromWho=fromWho,toWho=toWho) == 1 else False