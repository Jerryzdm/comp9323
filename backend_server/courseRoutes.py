from flask import request,jsonify
from globals import *
from sqlalchemy import desc
import json
from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis
from rediesConnecter import rd
from models import Follow
import time
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
from flask_script import Manager, Shell
from flask_mail import Mail, Message
from app import app, mail
from reviewAnalyzer import predict_sentiment
from course import *

api = Namespace('course', description='course operations')
def exportCourse(course):
    return {
        "courseId":course.courseId,
        "courseCode":course.courseCode,
        "courseName":course.courseName,
        "courseUrl": course.courseUrl,
        "courseUOC":course.courseUOC,
        "courseOverview":course.courseOverview,
        "courseFaculty":course.courseFaculty,
        "courseSchool":course.courseSchool,
        "courseStudyLevel":course.courseStudyLevel,
        "courseTerms":course.courseTerms,
        "courseCampus":course.courseCampus
    }


# reg_forms = api.model('reg_form', reg_form)
follow_forms = api.model('follow_form', follow_form)

@api.route('/<string:coursename>')
class CourseListByName(Resource):
    @api.doc(description="get course by name")
    def get(self,coursename):
        result = []

        try:
            lists = Course.query.filter(Course.courseCode == coursename).order_by(desc(Course.courseCode)).all()
            for course in lists:
                result.append(exportCourse(course))
            lists = Course.query.filter(Course.courseName.ilike("%" + coursename + "%")).order_by(desc(Course.courseCode)).all()
            for course in lists:
                result.append(exportCourse(course))
        except:
            return {"message": "bad payload"}, 400
        return result,200
@api.route('/subscribe')
class CourseSubscribeList(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.doc(description="Get current user's subscribe list")

    def get(self):
        try:
            current_user = get_jwt_identity()
        except:
            return {"message": "token"}, 400
        author = User.query.filter_by(username=current_user).first()
        result = []
        try:
            lists = Subscribe.query.filter(Subscribe.uid == author.id).all()
            for e in lists:
                result.append(e.cid)
            return result,200
        except:
            return {"message": "bad payload"}, 400




@api.route('/subscribe/<int:cid>')
class CourseSubscribe(Resource):
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.doc(description="to subscribe a crouse by courseId")
    def get(self,cid):
        try:
            current_user = get_jwt_identity()
        except:
            return {"message": "token"}, 400
        author = User.query.filter_by(username=current_user).first()

        try:
            lists = Subscribe.query.filter(Subscribe.cid == cid and Subscribe.uid == author.id).all()
            if(len(lists)==0):
                new_subscribe = Subscribe()
                new_subscribe.uid = author.id
                new_subscribe.cid = cid
                course = Course.query.filter(Course.courseId==cid).first()
                print(course)
                if not course:
                    return {"message": "no such course"}, 400
                print(course.courseCode)
                print(course.courseName)

                request_order = {'course_code': course.courseCode, 'term': "Term2", 'phase': 'Postgraduate',
                                 'email': author.email,
                                 'query_type_flag': 'bind'}
                response_order = send_request(request_order)


                db.session.add(new_subscribe)
                db.session.commit()
                return {"message": "subscribed"}, 201
            else:
                print("already subscribed")
                return {"message": "already subscribed"}, 400
        except:
            return {"message": "bad payload"}, 400

resource_fields = api.model('commsnts_form', commsnts_form)


def commentExporter(comment):
    return {"reviewId": comment.reviewId,
            "authorId": comment.authorId,
            "content": comment.content,
            "date": comment.date.timestamp(),
            "sentiment": comment.sentiment,
            "authorType": comment.authorType,
            "authorName": comment.authorName,
            "reply_to": comment.reply_to
            }
@api.route('/<int:cid>/reviews')
class CourseSubscribe(Resource):
    @api.doc(description="get course review by course id")
    def get(self,cid):
        result = []
        try:
            comment_list = Review.query.filter_by(reply_to=cid)
            for comment in comment_list:
                result.append(commentExporter(comment))
        except:
            return {"message": "bad payload"}, 400
        return result, 200

    @jwt_required
    @api.param("Authorization", _in='header')
    @api.doc(description="to add a review to a course")
    @api.expect(resource_fields)
    def post(self, cid):
        try:
            r = request.data.decode()
            r = json.loads(r)
            current_user = get_jwt_identity()
        except:
            return {"message": "token"}, 400
        author = User.query.filter_by(username=current_user).first()

        try:
            comment = Review()
            comment.authorName = current_user
            comment.authorId = author.id
            comment.content = r['content']
            comment.sentiment = predict_sentiment(r['content'])
            #comment.sentiment = 1
            comment.reply_to = r['reply_to']
            db.session.add(comment)
            db.session.commit()
            db.session.refresh(comment)
        except:
            return {"message": "bad payload"}, 400
        return {"cid": comment.reviewId}, 201


class CourseList(Resource):
    @api.doc(description="get course list")
    def get(self):
        result = []
        try:
            lists = Course.query.order_by(desc(Course.courseCode)).all()
            for course in lists:
                result.append(exportCourse(course))

        except:
            return {"message": "bad payload"}, 400
        return result,200

    @api.doc(
        description="User could follow a course\nWhen this course is available for registering\nThe user would receive an email that remind him to register.")
    @jwt_required
    @api.param("Authorization", _in='header')
    @api.expect(follow_forms)
    def post(self):
        current_user = get_jwt_identity()
        # try:
        r = request.data.decode()
        r = json.loads(r)
        new_follow = Follow()
        user = User.query.filter_by(username=current_user).first()
        new_follow.username = current_user
        new_follow.userId = user.id
        new_follow.email = user.email
        new_follow.courseCode = r['course_code']
        new_follow.courseName = r['course_name']
        db.session.add(new_follow)
        db.session.commit()
        db.session.refresh(new_follow)
        print(new_follow.followId)
        request_order = {'course_code': new_follow.courseCode, 'term': 1, 'phase': 'Postgraduate', 'email': new_follow.email,
                         'query_type_flag': 'bind'}
        response_order = send_request(request_order)
        return {'fid': new_follow.followId,
               }, 201


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def sendEmail(capacity, coursecode, email,flag):
    if flag == 'available_mess':
        msg = Message('Registering', sender='2457937678@qq.com', recipients=[email])
        msg.body = 'hello! The number of enrols for the course %s is %s now. It"s available for registering.' \
                   % (coursecode, capacity)
        send_async_email(app, msg)
    elif flag == 'comfirm_mess':
        msg = Message('Registering', sender='2457937678@qq.com', recipients=[email])
        msg.body = 'Hello! Your %s space monitoring has been confirmed now! %s has %s' % (coursecode,coursecode,capacity)
        send_async_email(app, msg)

api.add_resource(CourseList, '')
