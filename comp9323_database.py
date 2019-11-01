import sqlite3
from sqlite3 import Error


#create the database
def create_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        create_table_target_type = """CREATE TABLE IF NOT EXISTS target_type_table(
                                        targetID integer primary key AUTOINCREMENT,
                                        targetname text NOT NULL                            
                            ); """
        cur.execute(create_table_target_type)
        print('create_table_target_type!')

        create_table_user = """CREATE TABLE IF NOT EXISTS user_table(
                                        userID integer primary key AUTOINCREMENT,
                                        user_type text NOT NULL,
                                        user_like integer,
                                        username text NOT NULL UNIQUE,
                                        password text NOT NULL,
                                        email text NOT NULL UNIQUE,
                                        priority integer NOT NULL,
                                        user_studying_phase text
                                        ); """
        cur.execute(create_table_user)
        print('create_table_user!')

        create_table_post = """CREATE TABLE IF NOT EXISTS post_table(
                                        postID integer primary key AUTOINCREMENT,
                                        post_content text NOT NULL,
                                        post_title text NOT NULL,
                                        date_time time,
                                        post_status text NOT NULL,
                                        post_like integer,
                                        studying_phase text NOT NULL,
                                        post_unlike integer,
                                        userID references user_table(userID),
                                        targetID references target_type_table(targetID)
                            ); """
        cur.execute(create_table_post)
        print('create_table_post!')


        create_post_reply = """CREATE TABLE IF NOT EXISTS post_reply_table(
                                        replyid integer primary key AUTOINCREMENT,
                                        date_time time,
                                        reply_status text NOT NULL,
                                        reply_content text NOT NULL,
                                        userID references user_table(userID),
                                        postID references post_table(postID)                                   
                            ); """
        cur.execute(create_post_reply)
        print('create_table_post_reply!')

        conn.commit()
        conn.close()
        print("DONE!")
    except Error as e:
        print("Error on Sql", e)

if __name__ == '__main__':
    create_db('comp9323_forum.db')
