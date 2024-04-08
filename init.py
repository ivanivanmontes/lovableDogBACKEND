# from main import app
from flask import Flask
from flask_cors import CORS
app = Flask("__main__")
CORS(app)