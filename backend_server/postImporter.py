import csv
from models import *
from rediesConnecter import rd

csvPath = 'post_reply.csv'
def postImporter():
    with open(csvPath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            new_post = Post()
            new_post.authorName = "admin"
            new_post.authorId = 1
            new_post.authorType = 1
            new_post.content = row[2]
            new_post.title = row[1]
            new_post.date = datetime.now()
            l = []
            l.append(row[-1])
            new_post.tags = ",".join(l)
            new_post.priority = 1
            db.session.add(new_post)
            db.session.commit()
            rd.sadd(str(row[-1]), new_post.postId)
            rd.smembers(str(row[-1]))
            db.session.refresh(new_post)
            comment = Comment()
            comment.authorName = "admin"
            comment.authorId = 1
            comment.content = row[3]
            comment.reply_to =new_post.postId
            db.session.add(comment)
            db.session.commit()

