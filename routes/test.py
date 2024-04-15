import psycopg2
from main import app
from init import connection
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
        cur = connection.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()[0]
        cur.close()
        
        return f"Connected to PostgreSQL! Database version: {db_version}"
    
    except psycopg2.Error as e:
        # Handle any errors that occur during database connection
        return f"Error connecting to PostgreSQL: {e}"
    

@app.route("/addPin", methods =["POST"])
def add_pin() -> Response:
    """
    CREATE TABLE pins (
    Pin_ID INT PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    title VARCHAR(255),
    date_added DATE,
    description TEXT
);
    """
    data = request.get_json();
    pin_id = data.get("Pin_ID");
    latitude = data.get("latitude");
    longitude = data.get("longitude");
    title = data.get("title");
    date_added = data.get("date_added");
    desc = data.get("description")



    ...


@app.route("/getPins", methods = ["GET"])
def get_pins() -> Response:
    query = """
    SELECT *
    FROM pins
    """

    cur = connection.cursor()
    cur.execute(query)
    raw_data = cur.fetchall()
    return jsonify("success" , raw_data);


    




