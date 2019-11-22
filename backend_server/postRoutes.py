from flask import request,jsonify
from globals import *
import json
from sqlalchemy import desc
from flask_restplus import Api, Resource, fields, Namespace
from forms import *
from models import User
import redis

from rediesConnecter import rd

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
api = Namespace('posts', description='post operations')
postForm = api.model('post_form', post_form)
tagForm = api.model('post_form', tags_form)



@api.route('/<int:pid>')
class GetPost(Resource):
    @api.doc(
        description="Import a collection from the data service\nthe <collection> is collections in url\nThe database contains a table called collections, which has five properties, the primary key type is int, the remaining properties are type text type, and the json of \"entries\" is stored as strings.")

    def get(self,pid):
        print(pid)
        post = Post.query.filter_by(postId=pid).first()
        if not post:
            return {"message": "invalid pid"}, 400

        return {"postId": post.postId,
                "authorId": post.authorId,
                "content":post.content,
                "title": post.title,
                "date": post.date.timestamp(),
                "status": post.status,
                "authorType": post.authorType,
                "authorName": post.authorName,
                "priority": post.priority,
                "tags": post.tags.split(",")
                }, 200

    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(postForm)
    def put(self,pid):
        print(pid)
        post = Post.query.filter_by(postId=pid).first()
        if not post:
            return {"message": "invalid pid"}, 400
        current_user = get_jwt_identity()
        if current_user != post.authorName:
            return {"message": "invalid uid"}, 400
        try:
            r = request.data.decode()
            r = json.loads(r)
            post.content = r['content']
            post.title = r['title']
            post.tags = ",".join(r['tags'])
            db.session.commit()
            db.session.refresh(post)
        except:
            return {"message": "bad payload"}, 400
        return {"postId": post.postId,
                "authorId": post.authorId,
                "content": post.content,
                "title": post.title,
                "date": post.date.timestamp(),
                "status": post.status,
                "authorType": post.authorType,
                "authorName": post.authorName,
                "priority": post.priority,
                "tags": post.tags.split(",")
                }, 200
def jsontifyPostById(pid):
    post = Post.query.filter_by(postId=pid).first()
    if post:
        return {"postId": post.postId,
                "authorId": post.authorId,
                "content": post.content,
                "title": post.title,
                "date": post.date.timestamp(),
                "status": post.status,
                "authorType": post.authorType,
                "authorName": post.authorName,
                "priority": post.priority,
                "tags": post.tags.split(",")
                }
    else:
        return None
def jsontifyPost(post):
    if post:
        print(post.date.timestamp())
        return {"postId": post.postId,
                "authorId": post.authorId,
                "content": post.content,
                "title": post.title,
                "date": post.date.timestamp(),
                "status": post.status,
                "authorType": post.authorType,
                "authorName": post.authorName,
                "priority": post.priority,
                "tags": post.tags.split(",")
                }
    else:
        return None




@api.route('/tags')
class GetPostByTags(Resource):
    @api.expect(tagForm)
    def post(self):
        posts = []
        post_id_set = set()
        try:
            r = request.data.decode()
            r = json.loads(r)
            for tag in r['tags']:
                tmp_set = rd.smembers(tag)
                for pid in tmp_set:
                    post_id_set.add(pid)
            for pid in post_id_set:
                pid = int(pid)
                post = jsontifyPostById(pid)
                if post:
                    posts.append(post)
        except:
            return {"message": "bad tags"}, 400
        return posts, 201




@api.route('/all')
class GetALLPost(Resource):
    def get(self):
        posts = []
        try:
            query = db.session.query(Post)
            lists = query.filter(Post.status == 0).order_by(desc(Post.date)).all()
            for post in lists:
                posts.append(jsontifyPost(post))
        except:
            return {"message": "bad tags"}, 400
        return posts, 201



@api.route('')
class CreatePost(Resource):
    @api.doc(description="Import a collection from the data service\nthe <collection> is collections in url\nThe database contains a table called collections, which has five properties, the primary key type is int, the remaining properties are type text type, and the json of \"entries\" is stored as strings.")
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(postForm)
    def post(self):
        try:
            current_user = get_jwt_identity()
        except:
            return {"message": "token"}, 400
        try:
            r = request.data.decode()
            r = json.loads(r)
            new_post = Post()
            new_post.authorName = current_user
            author = User.query.filter_by(username=current_user).first()
            new_post.authorId = author.id
            new_post.authorType = author.user_type
            new_post.content = r['content']
            new_post.title = r['title']
            new_post.tags = ",".join(r['tags'])
            new_post.priority = 1
            new_post.date = datetime.now()
            db.session.add(new_post)
            db.session.commit()
            db.session.refresh(new_post,['postId'])
            print(new_post.postId)
            for e in r['tags']:
                rd.sadd(e, new_post.postId)
            for e in r['tags']:
                print(rd.smembers(e))
        except:
            return {"t": "input"}, 400
        return {'pid': new_post.postId,
               }, 201

@api.route('/search/<string:key>')
class Search(Resource):
    @api.doc(
        description="search post by key word")
    def get(self,key):
            result = []

            try:
                lists = Post.query.filter(Post.title.ilike("%" + key + "%")).order_by(desc(Post.date)).all()
                for course in lists:
                    result.append(jsontifyPost(course))
                lists = Post.query.filter(Post.content.ilike("%" + key + "%")).order_by(desc(Post.date)).all()
                for course in lists:
                    result.append(jsontifyPost(course))
            except:
                return {"message": "bad payload"}, 400
            return result, 200
