from sqlalchemy import  Column, Integer, String, ForeignKey, Text,DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(db.Integer, primary_key=True,autoincrement=True)
    username = Column(String(20),unique=True)
    _password = Column('password', db.String(128), nullable=False)
    faculty = db.Column(db.String(64))
    user_type = db.Column(db.String(64))
    email = db.Column(db.String(512))
    auth = db.Column(db.Integer, default="1")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, user_pwd):
        return check_password_hash(self._password, user_pwd)


class Post(db.Model):
    __tablename__ = 'posts'
    postId = Column(Integer, primary_key=True, autoincrement=True)
    authorId = Column(Integer)
    content = Column(Text)
    title = Column(String(128))
    date = Column(DateTime, default=datetime.now)
    status = Column(Integer, default=0)
    authorType = Column(String(64))
    authorName = Column(String(20))
    priority = Column(String(20))
    tags = Column(Text)

class Comment(db.Model):
    __tablename__ = 'comments'
    commentId = Column(Integer,primary_key=True)
    authorId = Column(Integer)
    content = Column(Text)
    date = Column(DateTime, default=datetime.now)
    authorType = Column(Integer, default=0)
    authorName = Column(String(64))
    reply_to = Column(Integer)

class Course(db.Model):
    __tablename__ = 'courses'
    courseId = Column(Integer,primary_key=True,autoincrement=True)
    courseCode = Column(String(20),unique=True)
    courseName = Column(String(128))
    courseUrl = Column(Text)
    courseUOC = Column(Integer)
    courseOverview = Column(Text)
    courseFaculty = Column(Text)
    courseSchool = Column(Text)
    courseStudyLevel = Column(Text)
    courseTerms = Column(Text)
    courseCampus = Column(Text)
    #repeateCourse = Column(Text)

class News(db.Model):
    __tablename__ = 'news'
    newsId = Column(Integer,primary_key=True,autoincrement=True)
    newsTitle = Column(String(100),unique=True)
    newsDate = Column(String(20))
    newsUrl = Column(Text)
    newsStandfirst = Column(Text)

class Follow(db.Model):
    followId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    email = Column(db.String(512))
    username = Column(String(20), unique=True)
    courseCode = Column(String(20),unique=True)
    courseName = Column(String(128))
    status = Column(Integer, default=1)


