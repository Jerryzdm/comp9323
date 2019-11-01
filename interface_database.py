import sqlite3
from sqlite3 import Error
from datetime import datetime

class interface_target_type_table:
    @staticmethod
    def insert(targetname):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False
        cur = conn.cursor()
        cur.execute("INSERT INTO target_type_table(targetID,targetname) VALUES (?,?)",(None,targetname))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def select_all():
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        cur = conn.cursor()
        cur.execute("SELECT * FROM target_type_table")
        conn.commit()
        result = cur.fetchall()
        keys = ['targetID', 'targetname']
        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def select(keyword=[],where=[]):
        if keyword!=[]:
            k = ""
            for i in keyword:
                k += i+","
            k = k[:-1]
        else:
            k = "*"
        if where !=[]:
            w = ""
            for j in where:
                w += j+" AND "
            w = w[:-5]
            q = "SELECT " + k + " FROM target_type_table WHERE " + w
        else:
            q = "SELECT " + k + " FROM target_type_table"
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False
        #print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        result = cur.fetchall()
        keys = ['targetID', 'targetname']
        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result


    @staticmethod
    def delete(self):
        pass


class interface_user_table():
    @staticmethod
    def insert(user_type,username,password,email,user_studying_phase=None):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False
        cur = conn.cursor()
        priority_dir = {'student':1,'staff':2,'manager':3}
        priority = priority_dir[user_type]
        user_status = 'actived'
        cur.execute("INSERT INTO user_table(userID,user_type,user_like,username,password,email,priority,user_studying_phase,user_status) VALUES (?,?,?,?,?,?,?,?,?)",
                    (None,user_type,0,username,password,email,priority,user_studying_phase,user_status))
        conn.commit()
        conn.close()
        return True


    @staticmethod
    def select_all():
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        cur = conn.cursor()
        cur.execute("SELECT * FROM user_table")
        conn.commit()
        result = cur.fetchall()
        keys = ['userID','user_type','user_like','username','password','email','priority','user_studying_phase','user_status']
        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def select(keyword=[],where=[]):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        if keyword!=[]:
            k = ""
            for i in keyword:
                k += i+","
            k = k[:-1]
        else:
            k = "*"
        if where !=[]:
            w = ""
            for j in where:
                w += j+" AND "
            w = w[:-5]
            q = "SELECT " + k + " FROM user_table WHERE " + w
        else:
            q = "SELECT " + k + " FROM user_table"

        #print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        result = cur.fetchall()
        keys = ['userID','user_type','user_like','username','password','email','priority','user_studying_phase','user_status']
        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def update(keyword=[],where=[]):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        if keyword!=[]:
            k = ""
            for i in keyword:
                k += i + ","
            k = k[:-1]
        else:
            k = "*"
        if where !=[]:
            w = ""
            for j in where:
                w += j+" AND "
            w = w[:-5]
            q = "UPDATE user_table SET " + k + " WHERE " + w
        else:
            q = "UPDATE user_table SET " + k
        #print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def unactived(where=[]):
        interface_user_table.update(["user_status='unactived'"],where)
        return True



class interface_post_table():
    @staticmethod
    def insert(post_content,post_title,targetname,username):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False
        cur = conn.cursor()
        date_time = datetime.now()
        targetID = interface_target_type_table.select(["targetID"],["targetname='%s'"%targetname])[0]["targetID"]
        userinfo = interface_user_table.select(["userID","user_studying_phase"],["username='%s'"%username])[0]
        #print(userinfo)
        userID = userinfo["userID"]
        studying_phase = userinfo["user_type"]
        post_status = 'actived'
        cur.execute("INSERT INTO post_table(postID,post_content,post_title,date_time,post_status,post_like,studying_phase,post_unlike,userID,targetID) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (None,post_content,post_title,date_time,post_status,0,studying_phase,0,userID,targetID))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def select_all():
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        cur = conn.cursor()
        cur.execute("SELECT * FROM post_table")
        conn.commit()
        result = cur.fetchall()
        keys = ['postID','post_content','post_title','date_time','post_status','post_like','studying_phase','post_unlike','userID','targetID']
        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def select(keyword=[], where=[]):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        if keyword != []:
            k = ""
            for i in keyword:
                k += i + ","
            k = k[:-1]
        else:
            k = "*"
        if where != []:
            w = ""
            for j in where:
                w += j + " AND "
            w = w[:-5]
            q = "SELECT " + k + " FROM post_table WHERE " + w
        else:
            q = "SELECT " + k + " FROM post_table"

        # print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        result = cur.fetchall()
        keys = ['postID', 'post_content', 'post_title', 'date_time', 'post_status', 'post_like', 'studying_phase',
                'post_unlike', 'userID','targetID']

        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def update(keyword=[], where=[]):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        if keyword != []:
            k = ""
            for i in keyword:
                k += i + ","
            k = k[:-1]
        else:
            k = "*"
        if where != []:
            w = ""
            for j in where:
                w += j + " AND "
            w = w[:-5]
            q = "UPDATE post_table SET " + k + " WHERE " + w
        else:
            q = "UPDATE post_table SET " + k
        #print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def unactived(where=[]):
        interface_post_table.update(["post_status='unactived'"], where)
        return True


class interface_post_reply_table():
    @staticmethod
    def insert(reply_content,userID,postID):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False
        cur = conn.cursor()
        date_time = datetime.now()
        reply_status = 'actived'
        cur.execute("INSERT INTO post_reply_table(replyid,date_time,reply_status,reply_content,userID,postID) VALUES (?,?,?,?,?,?)",
            (None,date_time,reply_status,reply_content,userID,postID))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def select_all():
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        cur = conn.cursor()
        cur.execute("SELECT * FROM post_reply_table")
        conn.commit()
        result = cur.fetchall()
        keys = ['replyid','date_time','reply_status','reply_content','userID','postID']
        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def select(keyword=[], where=[]):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        if keyword != []:
            k = ""
            for i in keyword:
                k += i + ","
            k = k[:-1]
        else:
            k = "*"
        if where != []:
            w = ""
            for j in where:
                w += j + " AND "
            w = w[:-5]
            q = "SELECT " + k + " FROM post_reply_table WHERE " + w
        else:
            q = "SELECT " + k + " FROM post_reply_table"

        # print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        result = cur.fetchall()
        keys = ['replyid','date_time','reply_status','reply_content','userID','postID']

        all_result = []
        for values in result:
            all_result.append(dict(zip(keys, values)))
        conn.close()
        return all_result

    @staticmethod
    def update(keyword=[], where=[]):
        try:
            conn = sqlite3.connect('comp9323_forum.db')
        except Error as e:
            print(e)
            return False

        if keyword != []:
            k = ""
            for i in keyword:
                k += i + ","
            k = k[:-1]
        else:
            k = "*"
        if where != []:
            w = ""
            for j in where:
                w += j + " AND "
            w = w[:-5]
            q = "UPDATE post_reply_table SET " + k + " WHERE " + w
        else:
            q = "UPDATE post_reply_table SET " + k
        #print(q)
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def unactived(where=[]):
        interface_post_reply_table.update(["reply_status='unactived'"], where)
        return True