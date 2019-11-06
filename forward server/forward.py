from flask import Flask, request,jsonify #import main Flask class and request object
import os
import dialogflow
import json

'''app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/forward')
def forward():
    text = request.args.get('Text')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth2.json"
    project_id = "try-webhook-qgfaam"
    session_id = "comp9323"
    language_code = "en"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response_dialogflow = session_client.detect_intent(session=session, query_input=query_input)
    print(response_dialogflow)
    return response_dialogflow


if __name__ == '__main_':
    app.run(port=40000)'''

app = Flask(__name__)


@app.route('/')
def index():
    return 'forward server'

@app.route('/forward')
def forward():
    print('get!!!!!')
    text = request.args.get('Text')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth2.json"
    project_id = "try-webhook-qgfaam"
    session_id = "comp9323"
    language_code = "en"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response_dialogflow = session_client.detect_intent(session=session, query_input=query_input)
    print((response_dialogflow.query_result.fulfillment_text))
    rsp=jsonify({'fulfillment_text':response_dialogflow.query_result.fulfillment_text})
    rsp.headers.add('Access-Control-Allow-Origin', '*')
    print(rsp)
    return rsp


if __name__ == '__name__':
    app.run()

app.run(port=4000)
