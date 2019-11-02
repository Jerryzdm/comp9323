from flask import request,jsonify
from globals import *
from sqlalchemy import desc
import json

from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis
from rediesConnecter import rd


from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
api = Namespace('course', description='course operations')

def exportCourse(course):
    return {
        "courseId":course.courseId,
        "courseCode":course.courseCode,
        "courseName":course.courseName,
        "courseUrl": course.courseUrl,
        "courseUOC":course.courseUOC,
        "repeateCourse": course.repeateCourse
    }


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
api.add_resource(CourseList, '')
