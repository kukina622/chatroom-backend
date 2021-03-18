from flask_restful import Resource, reqparse
from ..Model.user import UserModel
from flask import Request, session
from flask_login import login_user,logout_user,current_user
from .. import login_manager

class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username is required')
    parser.add_argument('password', required=True, help='Password is required')

    def post(self):
        arg = self.parser.parse_args()
        username = arg["username"]
        password = arg["password"]

        if not UserModel.is_exsit(username):
            return {"success": False}

        if UserModel.checkPassword(username, password):
            user = UserModel()
            user.id = username
            login_user(user)
            return {"success": True, "username": username}
        return {"success": False}


class register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username is required')
    parser.add_argument('password', required=True, help='Password is required')

    def post(self):
        arg = self.parser.parse_args()
        username = arg["username"]
        password = arg["password"]
        if UserModel.is_exsit(username):
            return {"success": False}
        UserModel.add_user(username, password)
        # UserModel.add_room(username, 0)  # 加到公開頻道
        return {"success": True}


class logout(Resource):
    def get(self):
        logout_user()
        return {"success": True}

class search(Resource):
    def get(self,searchUsername):
        if (UserModel.is_exsit(searchUsername)):
            userinfo_tmp=UserModel.searchUserinfo(searchUsername) #模糊查詢已註冊的用戶資料
            #查詢目前user送出的交友邀請&&條件to為searchUser
            sendInvitation=UserModel.sendInvitation(toWho=searchUsername,fromWho=current_user.id) 
            sendInvitation=list(map(lambda x: x[0],sendInvitation))
            userinfo=[]
            #將查詢到的用戶作整理
            for eachUser in userinfo_tmp:
                is_send=False
                #邀請是否有送出過
                if (eachUser[0] in sendInvitation):
                    is_send=True

                userinfo.append({"user":eachUser[0],"is_send":is_send})

            return {"success":True,"userinfo":userinfo}
        else:  
            return {"success":False}

class foo(Resource):
    def get(self):
        print(UserModel.is_invitationExist("A","B"))