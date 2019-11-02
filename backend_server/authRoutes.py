from flask import request,jsonify
import globals
import json
from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis
from datetime import timedelta
from app import jwt

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
api = Namespace('auth', description='Auth operations')
resource_fields = api.model('login_form', login_form)


class Login(Resource):
    @api.expect(resource_fields)
    def post(self):
        try:
            r = request.data.decode()
            username = json.loads(r)["username"]
            password = json.loads(r)["password"]
        except:
            return {"t": "input"}, 400
        user = User.query.filter_by(username=username).first()
        if not user.check_password(password):
            return {"message": "wrong password"}, 400
        access_token = create_access_token(identity=json.loads(r)["username"])
        refresh_token = create_refresh_token(identity=json.loads(r)["username"])

        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token
               }, 200


reg_forms = api.model('reg_form', reg_form)


class Reg(Resource):
    @api.expect(reg_forms)
    @api.doc(description="log in")
    def post(self):
        try:
            r = request.data.decode()
            print(json.loads(r))
            username = json.loads(r)["username"]
            password = json.loads(r)["password"]
            faculty = json.loads(r)["faculty"]
            user_type = json.loads(r)["user_type"]
            eamil = json.loads(r)["email"]
        except:
            return {"message": "wrong payload"}, 400
        user = User.query.filter_by(username=username).first()
        if user:
            return {"message": "wrong username"}, 400
        new_user = User()
        new_user.username = username
        new_user.password = password
        new_user.faculty = faculty
        new_user.user_type = user_type
        new_user.email = eamil
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=json.loads(r)["username"])
        refresh_token = create_refresh_token(identity=json.loads(r)["username"])
        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token
               }, 201


class LogOut(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    def delete(self):
        jti = get_raw_jwt()['Authorization']
        revoked_store.set(jti, 'true', timedelta(minutes=15) * 1.2)
        return jsonify({"msg": "Access token revoked"}), 200




api.add_resource(Reg, '/signup')
api.add_resource(Login, '/login')
api.add_resource(LogOut, '/logout')
