from flask_restplus import fields
#this is used for define request body structure
login_form =  {'username': fields.String(default='string: username', required=True),
        'password': fields.String(default='string: password',required=True),}

reg_form =  {'username': fields.String(default='string: username', required=True),
        'password': fields.String(default='string: password',required=True),
        'faculty': fields.String(default='string: CSE',required=True),
        'user_type': fields.String(default='string: Postgraduate',required=True),
        'email': fields.String(default='string: Postgraduate',required=True)
        }

post_form = {
        'title': fields.String(default='string: title', required=True),
        'content':fields.String(default='string: content', required=True),
        'tags':fields.List(fields.String,required=True)
}
tags_form = {
        'tags':fields.List(fields.String,required=True)
}

commsnts_form = {
        'content':fields.String(required=True),
        'reply_to':fields.Integer(required=True)
}

follow_form = {
        'course_code':fields.Integer(required=True),
        'course_name':fields.String(required=True)
}
