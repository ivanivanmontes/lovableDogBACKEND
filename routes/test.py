from main import app
from flask import jsonify, Response, request, session

# Define your route
@app.route('/')
def test():
    return 'hello world!'
