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
