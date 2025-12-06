from flask import Blueprint, request, jsonify
from database import get_connection
from email_service import send_checkout_email
import mysql.connector

transaction_bp = Blueprint("transaction_bp", __name__)

# checkout
@transaction_bp.route("/checkout", methods=["POST"])
def checkout():
    """
    Expects JSON:
    {
        "user_id": int,
        "items": [
            {"title": str, "author": str, "type": "buy"|"rent", "cost": float},
            ...
        ]
    }
    """
    data = request.json
    user_id = data.get("user_id")
    items = data.get("items", [])

    if not user_id or not items:
        return jsonify({"error": "Missing user_id or items"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        pending_items = []
        paid_items = []
        
        # Process each item
        for item in items:
            title = item.get("title")
            author = item.get("author")
            item_type = item.get("type")
            cost = item.get("cost")
            
            # Check current quantity for this book
            cursor.execute(
                "SELECT book_id, quantity FROM books WHERE title=%s AND author=%s",
                (title, author)
            )
            book = cursor.fetchone()
            
            if not book:
                # Book not found in inventory - still create transaction as pending
                status = 'pending'
                pending_items.append(title)
            elif book['quantity'] > 0:
                # Book available - decrease quantity and mark as paid
                # Only decrease quantity for "buy" transactions
                if item_type == 'buy':
                    cursor.execute(
                        "UPDATE books SET quantity = quantity - 1 WHERE book_id = %s AND quantity > 0",
                        (book['book_id'],)
                    )
                status = 'paid'
                paid_items.append(title)
            else:
                # Book out of stock - mark as pending
                status = 'pending'
                pending_items.append(title)
            
            # Insert transaction record
            query = """
                INSERT INTO transactions (user_id, book_title, author, type, cost, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (user_id, title, author, item_type, cost, status)
            cursor.execute(query, values)
        
        conn.commit()
        
        # Get user email for sending confirmation
        cursor.execute("SELECT username, email FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        
        # Calculate total
        total = sum(item['cost'] for item in items)
        
        # Send email if user has an email address
        email_sent = False
        if user and user.get('email'):
            email_sent, email_msg = send_checkout_email(
                customer_email=user['email'],
                customer_name=user['username'],
                items=items,
                total=total
            )
        
        # Build response message
        message = f"Checkout processed: {len(paid_items)} paid"
        if pending_items:
            message += f", {len(pending_items)} pending (out of stock)"
        if email_sent:
            message += ". Confirmation email sent!"
        
        return jsonify({
            "message": message,
            "paid_count": len(paid_items),
            "pending_count": len(pending_items),
            "pending_items": pending_items,
            "email_sent": email_sent
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# get all transactions (for manager)
@transaction_bp.route("/all", methods=["GET"])
def get_all_transactions():
    """Returns all transactions with user information."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT t.transaction_id, t.user_id, u.username, 
                   t.book_title, t.author, t.type, t.cost, 
                   t.status, t.created_at
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            ORDER BY t.created_at DESC
        """
        cursor.execute(query)
        transactions = cursor.fetchall()
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# get transactions for a specific user
@transaction_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_transactions(user_id):
    """Returns all transactions for a specific user."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT transaction_id, book_title, author, type, cost, 
                   status, created_at
            FROM transactions
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall()
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Update Transaction ----------------
@transaction_bp.route("/update/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    """Update transaction status."""
    data = request.json
    status = data.get("status")
    
    if not status or status not in ['pending', 'paid']:
        return jsonify({"error": "Invalid status. Must be 'pending' or 'paid'"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = "UPDATE transactions SET status = %s WHERE transaction_id = %s"
        cursor.execute(query, (status, transaction_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Transaction not found"}), 404
            
        return jsonify({"message": "Transaction updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()