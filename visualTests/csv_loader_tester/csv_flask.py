import sys

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from requestRelatedTests.calls.sendHttpCalls import sendFirebaseLessRequest

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
    result = sendFirebaseLessRequest(body=body)
    return jsonify(result.text)


def start_server():
    app.run(port=4608)


if __name__ == '__main__':
    start_server()
