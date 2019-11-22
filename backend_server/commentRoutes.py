from flask import request,jsonify
from globals import *
import json

from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis

from rediesConnecter import rd


from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
# set up name space
api = Namespace('comments', description='comments operations')
resource_fields = api.model('commsnts_form', commsnts_form)


class AddComment(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(resource_fields)
    @api.doc(description="add a comment to a post,will return a comment id")
    def post(self):
        try:
            r = request.data.decode()
            r = json.loads(r)
            current_user = get_jwt_identity()
            # get user info by token
            user = User.query.filter_by(username=current_user).first()
            # new a comment
            comment = Comment()
            comment.authorName = current_user
            comment.authorId = user.id
            comment.content =r['content']
            comment.reply_to = r['reply_to']
            # commit
            db.session.add(comment)
            db.session.commit()
            # refresh to get comment id
            db.session.refresh(comment)
        except:
            return {"message": "bad payload"}, 400
        return {"cid":comment.commentId},201
# return type
def commentExporter(comment):
    return {"commentId":comment.commentId,
                "authorId":comment.authorId,
                "content":comment.content,
                "date":comment.date.timestamp(),
                "authorType":comment.authorType,
                "authorName":comment.authorName,
                "reply_to":comment.reply_to
    }

@api.route('/<int:cid>')
class EditComment(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(resource_fields)
    @api.doc(description="edit a comment by comment id")
    def put(self,cid):
        try:
            r = request.data.decode()
            r = json.loads(r)
            current_user = get_jwt_identity()
            # get user info by token
            user = User.query.filter_by(username=current_user).first()
            # get comment
            comment = Comment.query.filter_by(commentId=cid).first()
            if user.id != comment.authorId:
                return {"message": "bad userid"}, 400
            comment.content = r['content']
            # commit
            db.session.commit()
        except:
            return {"message": "bad payload"}, 400
    @api.doc(description="delete a comment by comment id")
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(resource_fields)
    def delete(self,cid):
        try:
            r = request.data.decode()
            r = json.loads(r)
            # get user info by token
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
            # get comment
            comment = Comment.query.filter_by(commentId=cid).first()
            if user.id != comment.authorId:
                return {"message": "bad userid"}, 400
            # commit
            db.session.delete(comment)
            db.session.commit()
        except:
            return {"message": "bad payload"}, 400

    @api.doc(description="get a list fo comment by post id")
    def get(self,cid):
        result = []
        try:
            comment_list = Comment.query.filter_by(reply_to=cid)
            for comment in comment_list:
                result.append(commentExporter(comment))
        except:
            return {"message": "bad payload"}, 400
        return result,200

@api.route('/users/<int:uid>')
class EditComment(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.doc(description="get a list fo comment by user id")
    def get(self,uid):
        result = []
        try:
            comment_list = Comment.query.filter_by(authorId=uid)
            for comment in comment_list:
                result.append(commentExporter(comment))
        except:
            return {"message": "bad payload"}, 400
        return result, 200

api.add_resource(AddComment, '')

