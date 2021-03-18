import pymysql

db_settings = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "port": ,
    "charset": "utf8"
}

conn = pymysql.connect(**db_settings)


class db:

    global conn
    @staticmethod
    def store(username, password):
        with conn.cursor() as cursor:
            command = "INSERT INTO `users`(`username`,`password`)VALUES(%s,%s)"
            cursor.execute(command, (username, password))
        conn.commit()
      
    @staticmethod
    def searchExistUser(username):
        with conn.cursor() as cursor:
            command = '''
            SELECT EXISTS
            (SELECT `username` FROM users
            WHERE `username` = %s)'''
            cursor.execute(command, (username))
            return cursor.fetchall()[0][0]
            
    @staticmethod
    def searchPassword(username):
        with conn.cursor() as cursor:
            command = '''
            SELECT `password` FROM users
            WHERE `username` = %s'''
            cursor.execute(command, (username))
            return cursor.fetchall()[0][0]
    
    @staticmethod
    def storeRoom(username, room_id):
        with conn.cursor() as cursor:
            command = "INSERT INTO `rooms`(`username`,`room_id`)VALUES(%s,%s)"
            cursor.execute(command, (username, room_id))
        conn.commit()
    
    @staticmethod
    def searchRoom(username):
        roomList=[]
        with conn.cursor() as cursor:
            command = "SELECT `friend_id`,`user_2` FROM `friends` WHERE `user_1`= %s"
            cursor.execute(command, (username))
            [roomList.append({"room_id":x[0],"username":x[1]}) for x in cursor.fetchall()]
            command = "SELECT `friend_id`,`user_1` FROM `friends` WHERE `user_2`= %s"
            cursor.execute(command, (username))
            [roomList.append({"room_id":x[0],"username":x[1]}) for x in cursor.fetchall()]
        return roomList

    @staticmethod
    def storeRecord(room,message,fromWho,time):
        with conn.cursor() as cursor:
            command="INSERT INTO `records`(`room_id`,`message`,`from`,`time`) VALUES (%s,%s,%s,%s)"
            cursor.execute(command,(room,message,fromWho,time))
        conn.commit()

    @staticmethod
    def searchChatHistory(room):
        with conn.cursor() as cursor:
            command="SELECT * FROM `records` WHERE `room_id`= %s ORDER BY `time` ASC"
            cursor.execute(command,room)
            return cursor.fetchall()

    #查詢用戶
    @staticmethod
    def searchUser(username):
        username=username+"%"
        with conn.cursor() as cursor:
            command="SELECT `username` FROM `users` WHERE `username`LIKE %s"
            cursor.execute(command,username)
            return cursor.fetchall()

    #送出交友邀請
    @staticmethod
    def storeInvitation(fromWho,toWho):
        with conn.cursor() as cursor:
            command = "INSERT INTO `invitations`(`from`,`to`) VALUES (%s,%s)"
            cursor.execute(command, (fromWho, toWho))
        conn.commit()

    #查詢用戶時查詢已傳送的邀請
    @staticmethod
    def searchInvitation(searchUsername,nowUser):
        searchUsername=searchUsername+"%"
        with conn.cursor() as cursor:
            command="SELECT distinct `to` FROM `invitations` WHERE `to` LIKE %s and `from`= %s"
            cursor.execute(command,(searchUsername,nowUser))
            return cursor.fetchall()

    @staticmethod
    def delInvitation(fromWho,toWho):
        with conn.cursor() as cursor:
            command = "DELETE FROM `invitations` WHERE `from`=%s and `to`=%s"
            cursor.execute(command, (fromWho, toWho))
        conn.commit()

    #初始化時查詢
    @staticmethod
    def searchFriendInvitation(username):
        with conn.cursor() as cursor:
            command = "SELECT `from` FROM `invitations` WHERE `to` = %s"
            cursor.execute(command, (username))
            return cursor.fetchall()

    @staticmethod
    def storeFriend(user_1,user_2):
        with conn.cursor() as cursor:
            command = "INSERT INTO `friends`(`user_1`,`user_2`) VALUES (%s,%s)"
            cursor.execute(command, (user_1, user_2))
        conn.commit()
        with conn.cursor() as cursor:
            command = "SELECT `friend_id` FROM `friends` WHERE `user_1`= %s and `user_2`= %s"
            cursor.execute(command, (user_1, user_2))
            return cursor.fetchall()[0][0]
    
    @staticmethod
    def searchExistInvitation(fromWho,toWho):
        with conn.cursor() as cursor:
            command = '''
            SELECT EXISTS
            (SELECT `from`,`to` FROM `invitations`
            WHERE `from` = %s and `to`=%s)'''
            cursor.execute(command, (fromWho,toWho))
            return cursor.fetchall()[0][0]