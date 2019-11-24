import flask
import requests
from flask import Flask, request, make_response, jsonify
import json
from socket import *
from bs4 import BeautifulSoup
import urllib.request
from bs4 import BeautifulSoup
import time
import urllib.request
# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
    return 'Hello World!'


# function for responses
def results():
    def encode_request(pack):
        pack_j = json.dumps(pack)
        encode_pack = pack_j.encode('UTF-8')
        return encode_pack

    # decode_pack, bytes -> json_str -> dict
    def decode_response(pack):
        decode_pack = pack.decode('UTF-8')
        return json.loads(decode_pack)

    # send request_order
    def send_request(request_order):
        serverName = '127.0.0.1'
        serverPort = 12000  # change this port number if required
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        request_pack = encode_request(request_order)

        clientSocket.send(request_pack)
        response_pack = clientSocket.recv(1024)
        response_order = decode_response(response_pack)

        print('From Server:', response_order)
        clientSocket.close()
        return response_order

    def get_info_house(input_requset_dir):

        def make_url(input_requset_dir):
            url = 'https://www.realestate.com.au/rent/property-%s-between-%s-%s-in-%s/list-1?maxBeds=%s&source=refinement' \
                  % (input_requset_dir['propertyType'], input_requset_dir['minPrice'],
                     input_requset_dir['maxPrice'], input_requset_dir['where'], input_requset_dir['maxBeds'])
            return url

        def congure_set(url):
            page = urllib.request.urlopen(url)
            contents = page.read()
            bs = BeautifulSoup(contents, "html.parser")
            return bs

        def get_house_info(url):
            bs = congure_set(url)
            body = bs.body

            icon_info = body.find('ul', {'class': 'general-features rui-clearfix'})
            all_features = icon_info.find_all('li', {'class': 'general-features__feature'})

            beds = all_features[0]['aria-label']
            try:
                bathrooms = all_features[1]['aria-label']
            except:
                bathrooms = '0 bathrooms'
            try:
                cars = all_features[2]['aria-label']
            except:
                cars = '0 parking'

            addr = body.find('h1', {'class': 'property-info-address'}).string
            type = body.find('span', {'class': 'property-info__property-type'}).string
            price = body.find('span', {'class': 'property-price property-info__price'}).string
            dir = {'price': price, 'type': type, 'addr': addr, 'beds': beds, 'bathrooms': bathrooms, 'cars': cars,
                   'url': url}
            return dir

        url = make_url(input_requset_dir)
        bs = congure_set(url)
        body = bs.body
        # print(body)
        links = body.find('div', {'class': 'tiered-results tiered-results--exact'})
        all_links = links.find_all('a')
        # print(links)
        main_url = 'https://www.realestate.com.au'
        respo_info = []
        kk = []
        for i in all_links:
            new_link = main_url + i['href']
            if new_link not in kk:
                kk.append(new_link)
                try:
                    dir = get_house_info(new_link)
                    respo_info.append(dir)
                except:
                    pass
                if len(respo_info) == 5:
                    break
        return respo_info

    req = request.get_json(force=True)
    print(req)
    intent = req['queryResult']['intent']['displayName']
    print(intent)
    if intent == 'Default Welcome Intent':
        return {
            'fulfillmentText': 'Hi!<br>\n Welcome to UNSW Campus Experience Assistant!<br>\nBy sending "recent news", you can get the latest campus news!<br>\nBy sending "search question by title" you can search for questions in our online Q&A forum.<br>\nBy sending "check course information" you can get information and student\'s feedback of course you are interested in.<br>\n By sending "check course capacity",you can check the capacity of the course you are interested in.'}
    if intent == 'RecentNews':
        url = 'http://127.0.0.1:5000/news'
        response = requests.get(url=url)
        returnList=response.json()[:5]
        returnString=''
        for news in returnList:
            newsString=f"[Title]: {news['newsTitle']} <br>\n[Url]: {news['newsUrl']} <br>\n=================== <br>\n"
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
                returnString=f"[Course Code]: {course['courseCode']} <br>\n[Course Name]: {course['courseName']} <br>\n[UOC]: {course['courseUOC']} <br>\n[Url]: {course['courseUrl']}"
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
                    postString=f"[Title]: {post['title']}<br>\n [Content]: {post['content']} <br>\n[Url]: http://localhost:8080/detailpage/{post['postId']} <br>\n=================== <br>\n"
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
                postString = f"[Title]: {post['title']} <br>\n [Content]: {post['content']} <br>\n[Url]: http://localhost:8080/detailpage/{post['postId']} <br>\n=================== <br>\n"
                returnString += postString
        if returnString=='':
            return {'fulfillmentText': f"Sorry, no post tagged with {Tag} cannot be found, please try again"}
        return {'fulfillmentText': returnString}

    if intent == 'CheckCourseCapacity':
        print('hit!')
        Term = f"Term{req['queryResult']['parameters']['Term']}"
        CourseCode = req['queryResult']['parameters']['CourseCode']
        Phase=req['queryResult']['parameters']['phase']
        term = Term  # 'Term1' or 'Term2' or 'Term3' or 'Summer'
        course_code = CourseCode
        phase = Phase  # 'Undergraduate' or 'Postgraduate'
        email = ''
        query_type_flag = 'unbind'  # 'bind' or 'unbind'
        request_order = {'course_code': course_code, 'term': term, 'phase': phase, 'email': email,
                         'query_type_flag': query_type_flag}
        print(request_order)
        response_order = send_request(request_order)

        if response_order['all_result'] == []:
            return {'fulfillmentText': f'There is no {phase} course called {CourseCode} in {Term}, please try again.'}
        capacity = response_order['all_result'][0][7]
        capacity_cur,capacity_max=capacity.split(' / ')
        capacity_cur=int(capacity_cur)
        capacity_max=int(capacity_max)
        if capacity_cur==capacity_max:
            return {'fulfillmentText': f'{capacity} students is enrolling in {CourseCode} of {Term} in 2020. <br>\nIt\'s full, do you want to subscribe this course? <br>\nWe can send email notification once there are space in the course'}
        else:
            return {'fulfillmentText': f'{capacity} students is enrolling in {CourseCode} of {Term} in 2020. There are still some space in this course.'}
    if intent == 'CheckCourseCapacity - yes':
        print(req)
        email=req['queryResult']['outputContexts'][0]['parameters']['email']
        Term = f"Term{req['queryResult']['outputContexts'][0]['parameters']['Term']}"
        CourseCode = req['queryResult']['outputContexts'][0]['parameters']['CourseCode']
        Phase = req['queryResult']['outputContexts'][0]['parameters']['phase']
        term = Term  # 'Term1' or 'Term2' or 'Term3' or 'Summer'
        course_code = CourseCode
        phase = Phase  # 'Undergraduate' or 'Postgraduate'
        email = email
        query_type_flag = 'bind'  # 'bind' or 'unbind'
        request_order = {'course_code': course_code, 'term': term, 'phase': phase, 'email': email,
                         'query_type_flag': query_type_flag}
        response_order = send_request(request_order)
        return {'fulfillmentText': f'{CourseCode} of {Term} {Phase} has been subscribed with your email address {email}.'}
    if intent == 'CheckCourseCapacity - yes':
        return {'fulfillmentText': f'Alright, maybe you can try this next time.'}

    if intent == 'SearchRestaurantsAround':
        print(req['queryResult']['parameters'])
        l=['all','hotdogs', 'japanses', 'chinese', 'breakfast_brunch', 'bars', 'coffee', 'korean', 'burgers', 'italian']
        d=dict()
        for i in range(0,len(l)):
            d[str(i)]=l[i]
        Category= d[req['queryResult']['parameters']['Category']]
        response = requests.get('https://api.yelp.com/v3/businesses/search', headers={
                'Authorization': 'Bearer wsxgM4yqgWFodrULG1_6DquvBEDUyQys_CVtvgLFv7em_0lluU-Rw389FOn6Cb0IZpI7xRouvla_jCZbRK1CkhD8eKvOu7KTDPjjEUDF_FbGvSkvVkx9ZZlRrtDXXXYx'},
                                    params={'location': 'University Of New South Wales', 'radius': 1000, 'limit': 50,
                                            'sort_by': 'distance', 'categories': Category}).json()
        if len(response['businesses'])>5:
            out=response['businesses'][0:5]
        else:
            out=response['businesss']
        out=sorted(out,key=lambda x:x['rating'],reverse=True)
        returnString=""
        for ele in out:
            restString=f"[name]: {ele['name']} <br>\n[url]: {ele['url']} <br>\n[rating]: {ele['rating']} <br>\n['address']:{ele['location']['address1']} {ele['location']['address2']} {ele['location']['address1']} <br>\n=================== <br>\n"
            returnString+=restString
        return {'fulfillmentText': f'{returnString}'}

    if intent=='getAccomendation':
        d={'0':'house','1':'unit+apartment ','2':'townhouse','3':'villa'}
        where=req['queryResult']['parameters']['where']
        propertyType = d[req['queryResult']['parameters']['propertyType']]
        minPrice = req['queryResult']['parameters']['minPrice']
        maxPrice = req['queryResult']['parameters']['maxPrice']
        maxBeds = req['queryResult']['parameters']['maxBeds']
        input_requset_dir={'where':where,'minPrice':minPrice,'maxPrice':maxPrice,'propertyType':propertyType,'maxBeds':maxBeds}
        respo_info = get_info_house(input_requset_dir)
        if respo_info==[]:
            return {'fulfillmentText': f'Sorry there is no property matches your demand.'}
        returnString=''
        for i in respo_info:
            propString=f"[Address]:{i['addr']} <br>\n[price]:{i['price']} <br>\n[type]:{i['type']} <br>\n[beds]:{i['beds']} <br>\n[bathrooms]:{i['bathrooms']} <br>\n[cars]:{i['cars']} <br>\n[url]:{i['url']} <br>\n=================== <br>\n"
            returnString+=propString

        return {'fulfillmentText': f'{returnString}'}





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
    app.run(host= '0.0.0.0',port=6000)
