import sys
import fix_imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from requestRelatedTests.calls.sendHttpCalls import sendFirebaseLessRequest
from utils.corsBlocker import createResponseWithAntiCorsHeaders

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/getBotResponse', methods=['POST'])
def get_bot_response():
    print(list(sys.path))
    if request.method != 'POST':
        return 'Only POST requests are allowed.'
    try:
        body: str = request.get_json()
    except BadRequest:
        return "Message cannot be empty. Try sending a JSON object with any string message.", 400
    if isinstance(body, dict):
        body = body['body']
    requisitionResponse = sendFirebaseLessRequest(body=body)
    return createResponseWithAntiCorsHeaders(requisitionResponse.text)


def start_server():
    app.run(port=4608)


if __name__ == '__main__':
    start_server()
