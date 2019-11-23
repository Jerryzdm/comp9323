import os
import datetime
import redis

basedir = os.path.abspath(os.path.dirname(__file__))

# settings
class Config():
    os.environ.get("SECRET_KEY") or "you will never guess"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "minatoaqua"
    JWT_EXPIRATION_DELTA = datetime.timedelta(minutes=60)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '2457937678@qq.com'
    MAIL_PASSWORD = 'ieuhxafpzqhadjfj'
