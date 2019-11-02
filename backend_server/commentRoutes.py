from flask import request,jsonify
from globals import *
import json

from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis

host = '127.0.0.1'
port = 6379
rd = redis.Redis(host=host, port=port)

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
api = Namespace('comments', description='comments operations')
resource_fields = api.model('commsnts_form', commsnts_form)


class AddComment(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(resource_fields)
    def post(self):
        try:
            r = request.data.decode()
            r = json.loads(r)
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
            comment = Comment()
            comment.authorName = current_user
            comment.authorId = user.id
            comment.content =r['content']
            comment.reply_to = r['reply_to']
            db.session.add(comment)
            db.session.commit()
            db.session.refresh(comment)
        except:
            return {"message": "bad payload"}, 400
        return {"cid":comment.commentId},201

@api.route('/<int:cid>')
class EditComment(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(resource_fields)
    def put(self,cid):
        try:
            r = request.data.decode()
            r = json.loads(r)
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
            comment = Comment.quert.filter_by(commentId=cid).first()
            if user.id != comment.authorId:
                return {"message": "bad userid"}, 400
            comment.content = r['content']
            db.session.commit()
        except:
            return {"message": "bad payload"}, 400

    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(resource_fields)
    def delete(self,cid):
        try:
            r = request.data.decode()
            r = json.loads(r)
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
            comment = Comment.quert.filter_by(commentId=cid).first()
            if user.id != comment.authorId:
                return {"message": "bad userid"}, 400
            db.session.delete(comment)
            db.session.commit()
        except:
            return {"message": "bad payload"}, 400
api.add_resource(AddComment, '')

