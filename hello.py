from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'testing 1 2 3...'