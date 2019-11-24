from flask_mail import Mail, Message
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def sendEmail(capacity, coursecode, email,flag):

    if flag == 'available_mess':
        print('available_Sent')
        msg = Message('Registering', sender='2457937678@qq.com', recipients=[email])
        msg.body = 'hello! The number of enrols for the course %s is %s now. It"s available for registering.' \
                   % (coursecode, capacity)
        send_async_email(app, msg)
    elif flag == 'comfirm_mess':
        print('comfirm_Sent')
        msg = Message('Registering', sender='2457937678@qq.com', recipients=[email])
        msg.body = 'Hello! Your %s space monitoring has been confirmed now! %s has %s' % (coursecode,coursecode,capacity)
        send_async_email(app, msg)