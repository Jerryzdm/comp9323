import csv
from models import *
csvPath = 'post_reply.csv'
def newsImporter():
    with open(csvPath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            news = News()
            news.newsTitle = row[1]
            news.newsDate = row[2]
            news.newsStandfirst = row[3]
            news.newsUrl = row[4]
            db.session.add(news)
        db.session.commit()
