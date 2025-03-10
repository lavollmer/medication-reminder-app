from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(_name_)
app.config['SECRET_KEY'] = ''

# database connection that connects to SQLite database
def get_db():
    conn = sqlite3.connect('medication_reminders.db')
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = generate_password_hash(data['password'])

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (?,?)", (email,password))
    conn.commit()

    return jsonify({"message": "USer registered successfully!"}), 201