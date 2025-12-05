from flask import Blueprint, request, jsonify
from database import get_connection

book_bp = Blueprint("book_bp", __name__)

# ---------------- Add New Book ----------------
@book_bp.route("/add", methods=["POST"])
def add_book():
    data = request.json

    required = ["title", "author", "price_buy", "price_rent", "quantity"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO books (title, author, price_buy, price_rent, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data["title"],
            data["author"],
            data["price_buy"],
            data["price_rent"],
            data["quantity"]
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Book added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Get All Books ----------------
@book_bp.route("/all", methods=["GET"])
def get_all_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM books ORDER BY book_id DESC")
        books = cursor.fetchall()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Update Book ----------------
@book_bp.route("/update/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    required = ["title", "author", "price_buy", "price_rent", "quantity"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE books
            SET title=%s, author=%s, price_buy=%s, price_rent=%s, quantity=%s
            WHERE book_id=%s
        """
        values = (
            data["title"],
            data["author"],
            data["price_buy"],
            data["price_rent"],
            data["quantity"],
            book_id
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Book updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
