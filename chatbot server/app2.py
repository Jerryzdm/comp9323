import flask
import requests
from flask import Flask, request, make_response, jsonify
import json
from socket import *
# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
    return 'Hello World!'


# function for responses
def results():
    def send_request(request_order):
        def encode_request(pack):
            pack_j = json.dumps(pack)
            encode_pack = pack_j.encode('UTF-8')
            return encode_pack

        # decode_pack, bytes -> json_str -> dict
        def decode_response(pack):
            decode_pack = pack.decode('UTF-8')
            return json.loads(decode_pack)

        serverName = '127.0.0.1'
        serverPort = 12000  # change this port number if required
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        request_pack = encode_request(request_order)

        clientSocket.send(request_pack)
        response_pack = clientSocket.recv(1024)
        response_order = decode_response(response_pack)

        clientSocket.close()
        return response_order

    req = request.get_json(force=True)
    print(req)
    intent = req['queryResult']['intent']['displayName']
    print(intent)
    if intent == 'Default Welcome Intent':
        return {
            'fulfillmentText': 'Hi! Welcome to UNSW Campus Experience Assistant!\nBy sending "recent news", you can get the latest campus news!\nBy sending "search question" you can search for questions in our online Q&A forum.\nBy sending "check course information" you can get information and student\'s feedback of course you are interested in.\n By sending "check course capacity",you can check the capacity of the course you are interested in.\nBy sending "Subscribe Course Capacity", you can subscribe to a course to monitor its course capacity change.'}
    if intent == 'RecentNews':
        url = 'http://127.0.0.1:5000/news'
        response = requests.get(url=url)
        returnList=response.json()[:5]
        returnString=''
        for news in returnList:
            newsString=f"Title: {news['newsTitle']}\nUrl: {news['newsUrl']}\n====================="
            returnString+=newsString
        print(returnString)
        return {'fulfillmentText': returnString}
    if intent == 'CheckCourseInfo':
        CourseCode = req['queryResult']['parameters']['CourseCode']
        url = f'http://127.0.0.1:5000/course'
        CourseResponse = requests.get(url=url)
        returnString=f"Sorry, no course called {CourseCode} cannot be found, please try again"
        for course in CourseResponse.json():
            if course['courseCode']==CourseCode:
                returnString=f"Course Code: {course['courseCode']}\nCourse Name: {course['courseName']}\nUrl: {course['courseUrl']}\nUOC: {course['courseUOC']}"
                print(returnString)
                break
        return {'fulfillmentText': returnString}
    if intent == 'SearchQuestion':
        Question = req['queryResult']['parameters']['Question']
        keywords=Question.split()
        url = f'http://127.0.0.1:5000/posts/all'
        response = requests.get(url=url)
        returnString =''
        relatedPosts=[]
        for post in response.json():
            for keyword in keywords:
                if len(relatedPosts)==5:
                    break
                if keyword in post['title']:
                    relatedPosts.append(post)
                    postString=f"Title: {post['title']}\n Content: {post['content']}\nUrl: http://127.0.0.1:5000/posts/{post['postId']}"
                    returnString+=postString
        if returnString=='':
            return {'fulfillmentText': f"Sorry, no post related with {Question} cannot be found, please try again"}
        return {'fulfillmentText': returnString}
    if intent == 'SearchQuestionByTag':
        Tag = req['queryResult']['parameters']['tag']
        url = f'http://127.0.0.1:5000/posts/all'
        response = requests.get(url=url)

        returnString = f"Sorry, no post tagged with {Tag} cannot be found, please try again"
        returnString = ''
        relatedPosts = []
        for post in response.json():
            if len(relatedPosts) == 5:
                break
            if Tag in post['tags']:
                relatedPosts.append(post)
                postString = f"Title: {post['title']}\n Content: {post['content']}\nUrl: http://127.0.0.1:5000/posts/{post['postId']}"
                returnString += postString
        if returnString=='':
            return {'fulfillmentText': f"Sorry, no post tagged with {Tag} cannot be found, please try again"}
        return {'fulfillmentText': returnString}

    if intent == 'CheckCourseCapacity':
        print('hit!')
        Term = f"Term{req['queryResult']['parameters']['Term']}"
        CourseCode = req['queryResult']['parameters']['CourseCode']
        request_order = [CourseCode, Term]
        response_order = send_request(request_order)
        print('!!!', response_order)
        print(response_order == [None])
        if response_order == [None]:
            return {'fulfillmentText': f'There is no course called {CourseCode} in term {Term}, please try again.'}
        capacity = response_order[0][7]
        return {'fulfillmentText': f'{capacity} students is enrolling in {CourseCode} of term {Term} in 2020.'}
    if intent == 'SubscribCourse':
        return {'fulfillmentText': 'SubscribCourse'}
    if intent == 'CancelCourseSubscription':
        return {'fulfillmentText': 'CancelCourseSubscription'}

    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))



# run the app
if __name__ == '__main__':
    app.run(port=6000)
