from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def start_server():
    app.run(port=4608)


if __name__ == '__main__':
    start_server()
