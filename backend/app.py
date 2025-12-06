from flask import Flask
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.transaction_routes import transaction_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(book_bp, url_prefix="/books")
app.register_blueprint(transaction_bp, url_prefix="/transactions")

if __name__ == "__main__":
    app.run(debug=True)