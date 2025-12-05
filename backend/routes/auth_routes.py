from flask import Blueprint, request, jsonify
from database import get_connection
import bcrypt
import mysql.connector

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "fail", "message": "Missing fields"}), 400

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, hashed_pw, "customer")  # default role
        )
        conn.commit()
    except mysql.connector.errors.IntegrityError:
        return jsonify({"status": "fail", "message": "Username already exists"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"status": "success"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({"status": "fail", "message": "User not found"}), 404

    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({
            "status": "success",
            "message": "Login OK",
            "role": user["role"]
        })
    else:
        return jsonify({"status": "fail", "message": "Incorrect password"}), 401