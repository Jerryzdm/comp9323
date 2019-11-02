import secrets
from models import *
from flask_restplus import Resource, abort, reqparse, fields


def gen_token():
    token = secrets.token_hex(32)
    while len(db.session.query(User).filter_by(curr_token=token).all())>0:
        token = secrets.token_hex(32)
    print(token)
    return token

def authorize(token):
    if not token:
        abort(403,'Unsupplied Authorization Token')
    try:
        token = token.split(" ")[1]
    except:
        abort(403,'Invalid Authorization Token')
    if not db.exists("USER").where(curr_token=token):
        abort(403,'Invalid Authorization Token')
    return db.select("USER").where(curr_token=token).execute()