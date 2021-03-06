from flask import request, jsonify
import globals
import json
from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis
from datetime import timedelta
from models import *
from app import jwt

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)

# set ACCESS TOKEN EXPIRES TIME
ACCESS_EXPIRES = timedelta(minutes=60)
REFRESH_EXPIRES = timedelta(days=30)

# link to redis to store token
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)

# init api namespace
api = Namespace('auth', description='Auth operations')
resource_fields = api.model('login_form', login_form)


# @api.doc(params={'id': 'An ID'})
class Login(Resource):
    @api.expect(resource_fields)
    @api.doc(description="login operation, will return a access token and a refresh token")
    def post(self):
        # decode request body
        try:
            r = request.data.decode()
            username = json.loads(r)["username"]
            password = json.loads(r)["password"]
        except:
            return {"t": "input"}, 400
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "wrong username"}, 400
        elif user and not user.check_password(password):
            return {"message": "wrong password"}, 400
        # gen token
        access_token = create_access_token(identity=json.loads(r)["username"])
        refresh_token = create_refresh_token(identity=json.loads(r)["username"])

        # check token
        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)

        # set expires time
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

        # return tokens
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token,
                   'uid': user.id
               }, 200


reg_forms = api.model('reg_form', reg_form)


class Reg(Resource):
    @api.expect(reg_forms)
    @api.doc(description="signon operation, will return a access token and a refresh token")
    def post(self):
        # decode request body
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
        # check if username already in database(it should be unique)
        user = User.query.filter_by(username=username).first()
        if user:
            return {"message": "wrong username"}, 400

        # gen new user
        new_user = User()
        new_user.username = username
        new_user.password = password
        new_user.faculty = faculty
        new_user.user_type = user_type
        new_user.email = eamil

        # commit new user to database
        db.session.add(new_user)
        db.session.commit()

        # gen token
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

@api.route('/users/<int:uid>')
class getUsersInfo(Resource):
    @api.doc(description="to get user information")
    def get(self,uid):
        user = User.query.filter_by(id=uid).first()
        if not user:
            return {"message": "wrong uid"}, 400
        else:
            return {"id":user.id,
                    "username":user.username,
                    "faculty":user.faculty,
                    "user_type":user.user_type,
                    "email":user.email
            },200



@api.route('/update')
class Update(Resource):
    @api.expect(reg_forms)
    @api.doc(description="to undate user information")
    @jwt_required
    @api.param("Authorization", _in='header')
    def post(self):
        # verify user token
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
        except:
            return {"message": "token"}, 400

        # decode request body
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

        # get user info
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "wrong username"}, 400

        # update user info
        user.username = username
        user.password = password
        user.faculty = faculty
        user.user_type = user_type
        user.email = eamil

        # commit changes
        db.session.commit()

        # gen an new set of token
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


class LogOut(Resource):
    @jwt_required
    @api.doc(description="m")
    @api.param("Authorization", _in='header')
    @api.doc(description="logout operation，revok the token")

    def delete(self):
        jti = get_raw_jwt()['Authorization']
        revoked_store.set(jti, 'true', timedelta(minutes=15) * 1.2)
        return jsonify({"msg": "Access token revoked"}), 200


api.add_resource(Reg, '/signup')
api.add_resource(Login, '/login')
api.add_resource(LogOut, '/logout')
