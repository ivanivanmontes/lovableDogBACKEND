import psycopg2
from main import app
from init import connection
from flask import jsonify, Response

url = "postgresql://postgres:2046@localhost:5432/test"

@app.route('/', methods=["GET"])
def test_connection() -> Response:
    return jsonify("connection successful", 200)

# DB test
@app.route('/dbtest')
def test_db_connection():
    try:
        cur = connection.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()[0]
        cur.close()
        
        return f"Connected to PostgreSQL! Database version: {db_version}"
    
    except psycopg2.Error as e:
        return f"Error connecting to PostgreSQL: {e}"
    