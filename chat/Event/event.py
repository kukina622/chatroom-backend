from flask_socketio import emit, join_room, leave_room
from .. import socketio
from datetime import datetime as dt
from .. import login_manager
from flask_login import current_user
from ..Model.user import UserModel
from ..Model.db import db
from flask import abort

@socketio.on('sendMessage')
def sendMessage(sendData):
    sendData = dict(sendData)
    sendData["datetime"] =dt.now().strftime("%Y-%m-%d %H:%M:%S")
    UserModel.add_record(sendData)
    emit("backMessage", sendData, room=sendData["room"])


@socketio.on("initConnect")
def initJoin():
    if current_user.is_authenticated:
        join_room(current_user.id) #加到"自己的username"的房間
        roomList=UserModel.allrooms(current_user.id)
        roomList.insert(0,{"room_id":0,"username":"公開頻道"})
        friendInvitationList=UserModel.allfriendInvitation(current_user.id) 
        chatHistoryDict={}
        for room in roomList:
            join_room(room["room_id"])
            allChatHistory=db.searchChatHistory(room["room_id"])
            chatHistoryDict[room["room_id"]]=[]
            for ChatHistory in allChatHistory:
                if (len(ChatHistory)==0):
                    continue
                tmp={"room":ChatHistory[0],"message":ChatHistory[1],"from":ChatHistory[2],"datetime":ChatHistory[3].strftime("%Y-%m-%d %H:%M:%S")}
                chatHistoryDict[room["room_id"]].append(tmp)
        
        allBackData={}
        allBackData["rooms"]=roomList
        allBackData["chatHistory"]=chatHistoryDict
        allBackData["friendInvitation"]=friendInvitationList
        emit('initChatroom',allBackData)
    

@socketio.on("acceptInvitation")
def acceptInvitation(username):
    room_id=UserModel.add_friend(username,current_user.id)
    invitation={"from":username,"to":current_user.id}
    UserModel.delInvitation(invitation)
    invitation["room_id"]=room_id
    join_room(room_id)
    emit("backAccept",invitation,room=username)
    emit("backAccept",invitation)


@socketio.on("rejectInvitation")
def rejectInvitation(username):
    invitation={"from":username,"to":current_user.id}
    UserModel.delInvitation(invitation)
    


@socketio.on("sendInvite")
def sendInvite(username):
    if (UserModel.is_exsit(username) and username!=current_user.id):
        invitation={"from":current_user.id,"to":username}
        if not UserModel.is_invitationExist(fromWho=username,toWho=current_user.id):
            UserModel.add_invitation(invitation)
            emit('backInvite',invitation["from"],room=invitation["to"])
        else:
            acceptInvitation(username)
            emit('backInviteDEL',invitation["from"])
        
    else:
        abort(404)
    
@socketio.on("cancelInvite")
def cancelInvite(username):
    invitation={"from":current_user.id,"to":username}
    UserModel.delInvitation(invitation)
    #傳送刪除事件
    emit('backInviteDEL',invitation["from"],room=invitation["to"])

@socketio.on('join')
def join(room_id):
    join_room(room_id)

@socketio.on("connect")
def connect():
    if not current_user.is_authenticated:
        return False
    print("connection")