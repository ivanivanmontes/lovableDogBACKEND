import psycopg2
import random
from main import app
from init import connection
from flask import jsonify, Response, request

url = "postgresql://postgres:2046@localhost:5432/test"

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
    try:
        data = request.get_json();
        # pin_id = data.get("Pin_ID");
        pin_id = random.randint(0, 1000000);
        latitude = data.get("latitude");
        longitude = data.get("longitude");
        title = data.get("title");
        date_added = data.get("date_added");
        desc = data.get("description");
        user_id = data.get("user_id");
        query = """
            INSERT INTO pins (Pin_ID, latitude, longitude, title, date_added, description, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        if user_id is None: return jsonify({"error" : "must pass in a user_id"});

        cur = connection.cursor()
        cur.execute(query, (pin_id, latitude, longitude, title, date_added, desc, user_id))  # Passing values as a tuple
        connection.commit();
        cur.close();

        return jsonify("success", 200);
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});

@app.route("/getPins/<int:user_id>", methods = ["GET"])
def get_pins(user_id : int) -> Response:
    query = """
    SELECT *
    FROM pins
    WHERE user_id = %s
    """
    try:
        cur = connection.cursor()
        cur.execute(query, (user_id,))
        raw_data = cur.fetchall()
        cur.close()
        column_name = [column[0] for column in cur.description]
        result = [dict(zip(column_name, row)) for row in raw_data]
        return jsonify(result);
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});

@app.route("/getPin/<int:pin_id>", methods=["GET"])
def get_pin(pin_id : int) -> Response:
    query = """
    SELECT *
    FROM pins 
    WHERE pin_id = (%s)
    """
    try:
        cur = connection.cursor()
        cur.execute(query, (pin_id,))
        raw_data = cur.fetchall()
        column_name = [column[0] for column in cur.description]
        result = [dict(zip(column_name, row)) for row in raw_data]
        cur.close()
        return jsonify(result);
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});

@app.route("/deletePin/<int:pin_id>", methods=["DELETE"])
def delete_pin(pin_id : int) -> Response:
    query = """
    DELETE 
    FROM pins
    WHERE pin_id = %s
    """
    try:
        cur = connection.cursor()
        cur.execute(query, (pin_id,))
        connection.commit()
        cur.close();
        return jsonify("success", 200)
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});

@app.route("/updatePin/<int:pin_id>", methods=["PUT"])
def update_pin(pin_id : int) -> Response:
    # what if only some parts of the pin information are updated?
    query = """
        UPDATE pins
        SET title = %s, description = %s, latitude = %s, longitude = %s
        WHERE pin_id = %s

    """
    try:
        data = request.get_json()
        latitude = data.get("latitude");
        longitude = data.get("longitude");
        new_title = data.get("title");
        new_desc = data.get("description");
        cur = connection.cursor()
        cur.execute(query, (new_title, new_desc, latitude, longitude, pin_id,))
        connection.commit()
        cur.close()

        return jsonify("success", 200);
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});
        



