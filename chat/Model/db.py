import pymysql

db_settings = {
    "host": "127.0.0.1",
    "user": "",
    "password": "",
    "database": "chatroom",
    "port":3306 ,
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
    def searchRoom(username):
        roomList=[]
        with conn.cursor() as cursor:
            command='''select `uid` from `users` where `username`= %s '''
            cursor.execute(command,username)
            uid=cursor.fetchone()[0]
            command = '''SELECT friend.friend_id,users.username from 
            (SELECT `friend_id`,`user_1` FROM `friends` WHERE `user_2`=%s
            UNION
            SELECT `friend_id`,`user_2` FROM `friends` WHERE `user_1`=%s) as friend
            INNER JOIN `users`
            ON friend.user_1=users.uid'''
            cursor.execute(command, (uid,uid))
            [roomList.append({"room_id":x[0],"username":x[1]}) for x in cursor.fetchall()]
        return roomList

    @staticmethod
    def storeRecord(room,message,fromWho,time):
        with conn.cursor() as cursor:
            command='''select `uid` from `users` where `username`= %s '''
            cursor.execute(command,fromWho)
            uid=cursor.fetchone()[0]
            command="INSERT INTO `records`(`room_id`,`message`,`from`,`time`) VALUES (%s,%s,%s,%s)"
            cursor.execute(command,(room,message,uid,time))
        conn.commit()

    @staticmethod
    def searchChatHistory(room):
        with conn.cursor() as cursor:
            command='''
            SELECT records.room_id,records.message,users.username,records.time 
            FROM `records`
            INNER JOIN `users`
            ON records.from = users.uid
            WHERE records.room_id= %s ORDER BY records.time ASC
            '''
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
            command ='''
            INSERT INTO `invitations`(`from`,`to`)
            SELECT a.uid,b.uid
            from (
            (SELECT `uid` from `users` WHERE `username`=%s) as a,
            (SELECT `uid` from `users` WHERE `username`=%s) as b
            )
            '''
            cursor.execute(command, (fromWho, toWho))
        conn.commit()
# 4/23 01:55

    #查詢用戶時查詢已傳送的邀請
    @staticmethod
    def searchInvitation(searchUsername,nowUser):
        searchUsername=searchUsername+"%"
        with conn.cursor() as cursor:
            command='''
                SELECT DISTINCT u.toName
                from
                (SELECT u1.username as toName,u2.username as fromName
                FROM `invitations`
                INNER JOIN `users`as u1
                ON u1.uid=invitations.to
                INNER JOIN `users`as u2
                ON u2.uid=invitations.from) as u
                WHERE u.toName like %s and u.fromName = %s
            '''
            cursor.execute(command,(searchUsername,nowUser))
            return cursor.fetchall()

    @staticmethod
    def delInvitation(fromWho,toWho):
        with conn.cursor() as cursor:
            command = "select `uid` from `users` where `username`= %s"
            cursor.execute(command,(fromWho))
            uid_from = cursor.fetchone()[0]
            cursor.execute(command,(toWho))
            uid_to = cursor.fetchone()[0]
            del_command="DELETE FROM `invitations` WHERE `from`=%s and `to` =%s"
            cursor.execute(del_command, (uid_from, uid_to))
        conn.commit()

    #初始化時查詢
    @staticmethod
    def searchFriendInvitation(username):
        with conn.cursor() as cursor:
            command = '''
                SELECT DISTINCT u.fromName
                from
                (SELECT u1.username as toName,u2.username as fromName
                FROM `invitations`
                INNER JOIN `users`as u1
                ON u1.uid=invitations.to
                INNER JOIN `users`as u2
                ON u2.uid=invitations.from) as u
                WHERE u.toName = %s
            '''
            cursor.execute(command, (username))
            return cursor.fetchall()

    @staticmethod
    def storeFriend(user_1,user_2):
        with conn.cursor() as cursor:
            command = '''INSERT INTO `friends`(`user_1`,`user_2`)
            SELECT u1.uid,u2.uid
            FROM
            (SELECT `uid` from `users` where `username`=%s) as u1,
            (SELECT `uid` from `users` where `username`=%s) as u2
            '''
            cursor.execute(command, (user_1, user_2))
        conn.commit()
        with conn.cursor() as cursor:
            command = '''
            SELECT friends.friend_id
            FROM `friends`
            inner JOIN `users` as u1
            ON friends.user_1=u1.uid
            inner JOIN `users` as u2
            ON friends.user_2=u2.uid
            WHERE u1.username = %s and u2.username = %s
            '''
            cursor.execute(command, (user_1, user_2))
            return cursor.fetchall()[0][0]
    
    @staticmethod
    def searchExistInvitation(fromWho,toWho):
        with conn.cursor() as cursor:
            command = '''
            SELECT EXISTS
            (SELECT u1.username,u2.username FROM `invitations`
            INNER JOIN `users` as u1
            on invitations.from = u1.uid
            INNER JOIN `users` as u2
            on invitations.to = u2.uid
            WHERE u1.username = %s and u2.username =%s)'''
            cursor.execute(command, (fromWho,toWho))
            return cursor.fetchall()[0][0]