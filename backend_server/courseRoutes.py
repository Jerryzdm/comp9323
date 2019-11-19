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




class CourseList(Resource):
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
        return {'fid': new_follow.followId,
               }, 201


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def sendEmail(capacity, coursecode, email):
    msg = Message('Registering', sender='2457937678@qq.com', recipients=[email])
    msg.body = 'hello! The number of enrols for the course %s is %s now. It"s available for registering.' \
               % (coursecode, capacity)
    send_async_email(app, msg)

api.add_resource(CourseList, '')
