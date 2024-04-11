import psycopg2
from flask import Flask
from flask_cors import CORS
app = Flask("__main__")
CORS(app)
# url = "postgres://dttccrum:XsuiMdrtUPYmWoTmH3wu7EIJkpTJ_FzU@bubble.db.elephantsql.com/dttccrum"
url = "postgresql://postgres:2046@localhost:5432/test"
connection = psycopg2.connect(url)