import psycopg2
import bcrypt
from main import app
from init import connection
from flask import jsonify, Response, request

url = "postgresql://postgres:2046@localhost:5432/test"

@app.route("/addUser", methods = ["POST"])
def add_user() -> Response:
    """
    CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
	username VARCHAR(255) NOT NULL,
	partner_id INT NULL,
	FOREIGN KEY (partner_id) REFERENCES users(user_id));
    """
    query = """
        INSERT INTO users (user_id, email, hashed_password, first_name, last_name, username)
        VALUES (%s, %s, %s, %s, %s, %s)
    
    """
    try:
        data = request.get_json();
        user_id = data.get("user_id");
        email = data.get("email")
        password = data.get("password");
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username");
        # every new user will not have a partner_id
        cur = connection.cursor()
        cur.execute(query, (user_id, email, hashed_password, first_name, last_name, username,))
        connection.commit()
        cur.close()
        return jsonify({"message": "User added successfully!"}), 200

    except psycopg2.Error as e:
        return jsonify(str(e), 400);

@app.route("/getUser/<int:user_id>", methods = ["GET"])
def get_user(user_id : int) -> Response:
    query = """
    SELECT *
    FROM users 
    WHERE user_id = %s
    """
    try: 
        cur = connection.cursor()
        cur.execute(query, (user_id,))
        raw_data = cur.fetchall()
        column_name = [column[0] for column in cur.description]
        result = [dict(zip(column_name, row)) for row in raw_data]
        cur.close()
        return jsonify(result);
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});

# @app.route("/updateUser/<int:user_id>", methods = ["PUT"])
# def update_user(user_id : int) -> Response:
#     Consider what it means to update a user...

@app.route("/deleteUser/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id : int) -> Response:
    query = """
    DELETE * 
    FROM users
    WHERE user_id = %s
    """
    try:
        cur = connection.cursor()
        cur.execute(query, (user_id,))
        connection.commit()
        cur.close()
        return jsonify("success", 200);
    except psycopg2.Error as e:
        return jsonify({"error" : str(e)});
