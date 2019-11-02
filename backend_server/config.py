import os
import datetime
import redis

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    os.environ.get("SECRET_KEY") or "you will never guess"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "minatoaqua"
    JWT_EXPIRATION_DELTA = datetime.timedelta(minutes=15)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
