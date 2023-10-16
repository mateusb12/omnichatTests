from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from requestTests.calls.sendHttpCalls import sendFirebaseLessRequest

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/getBotResponse', methods=['POST'])
def get_bot_response():
    if request.method != 'POST':
        return 'Only POST requests are allowed.'
    try:
        body: str = request.get_json()
    except BadRequest:
        return "Message cannot be empty. Try sending a JSON object with any string message.", 400
    return sendFirebaseLessRequest(body=body)


def start_server():
    app.run(port=4608)


if __name__ == '__main__':
    start_server()
