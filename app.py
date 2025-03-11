from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(_name_)
app.config["SECRET_KEY"] = ""


# database connection that connects to SQLite database
def get_db():
    conn = sqlite3.connect("medication_reminders.db")
    return conn


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data["email"]
    password = generate_password_hash(data["password"])

    # user information stored in the users table in database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, password) VALUES (?,?)", (email, password)
    )
    conn.commit()

    return jsonify({"message": "USer registered successfully!"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        token = jwt.encode(
            {
                "user_id": user[0],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/reminders', methods=['POST'])
def add_reminder():
    data = request.get_json()
    token = request.headers.get('Authorization').split()[1]  # Extract token from Authorization header

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401

    medication_name = data['medication_name']
    dosage = data['dosage']
    time = data['time']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (medication_name, dosage, time, user_id) VALUES (?, ?, ?, ?)",
                   (medication_name, dosage, time, user_id))
    conn.commit()

    return jsonify({"message": "Reminder added!"}), 201

@app.route('/reminders', methods=['GET'])
def get_reminders():
    token = request.headers.get('Authorization').split()[1]

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders WHERE user_id=?", (user_id,))
    reminders = cursor.fetchall()

    reminders_list = [{"medication_name": r[1], "dosage": r[2], "time": r[3]} for r in reminders]

    return jsonify(reminders_list), 200

if __name__ == '__main__':
    app.run(debug=True)