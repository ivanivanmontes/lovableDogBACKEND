import psycopg2
from main import app
from flask import jsonify, Response, request, session

url = "postgresql://postgres:2046@localhost:5432/test"

# Define your route
@app.route('/', methods=["GET"])
def test_connection() -> Response:
    return jsonify("connection successful", 200)

# DB test
@app.route('/dbtest')
def test_db_connection():
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(url)
        
        # Create a cursor to execute SQL queries
        cur = conn.cursor()
        
        # Execute a sample SQL query
        cur.execute("SELECT version()")
        
        # Fetch the result of the query
        db_version = cur.fetchone()[0]
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        return f"Connected to PostgreSQL! Database version: {db_version}"
    
    except psycopg2.Error as e:
        # Handle any errors that occur during database connection
        return f"Error connecting to PostgreSQL: {e}"