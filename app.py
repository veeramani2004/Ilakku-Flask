from config import Config
from flask import Flask

from extensions import db, jwt
from sqlalchemy.sql import text
from flask_cors import CORS

# from routes.movies_bp import movies_bp
from routes.users_bp import users_bp
from os import environ

app = Flask(__name__)
app.config.from_object(Config)  # URL
CORS(app)


db.init_app(app)  # Call
jwt.init_app(app)


@jwt.unauthorized_loader
def _unauth(e):
    return {"error": "missing/invalid token"}, 401


@jwt.expired_token_loader
def _expired(h, p):
    return ({"error": "token expired"}), 401


with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
    except Exception as e:
        print("Error connecting to the database:", e)


@app.get("/")
def hello_world():
    print("Super")
    return "<h1>Hello, World! 🎊🍊 🌽</h1>"


# app.register_blueprint(movies_bp, url_prefix="/api/movies")
app.register_blueprint(users_bp, url_prefix="/api/users")

# Deployment Steps
# 1. main.py -> app.py
# 2. As below
# 3. Install gunicorn (freeze, commit, push)
## Render
# 4. gunicorn app:app
# 5. Follow as readme
if __name__ == "__main__":
    port = environ.get("PORT", 5000)  # Auto assign port number (render.com)
    app.run(host="0.0.0.0", port=port, debug=True)  # Any ip address is accepted
