from flask import Flask
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    print("Backend running at http://127.0.0.1:5000")
    app.run(debug=True)