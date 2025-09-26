from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from routes.users_bp import users_bp
from routes.posts_bp import posts_bp
from os import environ
from routes.resources_bp import resources_bp
from routes.comments_bp import comments_bp
from routes.saved_posts_bp import saved_posts_bp
from routes.follow_bp import follow_bp
from routes.mentor_applications_bp import mentor_app_bp
from routes.admin_mentor_bp import admin_mentor_bp

app = Flask(__name__)
app.config.from_object("config.Config")


# CORS(
#     app,
#     resources={r"/api/*": {"origins": "http://localhost:5173"}},
#     supports_credentials=True,
# )

# Initialize DB and JWT
# Initialize DB and JWT
# CORS(
#     app,
#     origins=["http://localhost:5173"],
#     supports_credentials=True,
#     allow_headers=["Content-Type", "Authorization"],
#     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
# )
CORS(
    app,
    resources={r"/api/*": {"origins": ["http://localhost:5173"]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)


db.init_app(app)
jwt.init_app(app)


# JWT error handlers
@jwt.unauthorized_loader
def _unauth(e):
    return {"error": "missing/invalid token"}, 401


@jwt.expired_token_loader
def _expired(h, p):
    return {"error": "token expired"}, 401


# Register blueprints

app.register_blueprint(mentor_app_bp, url_prefix="/api/mentor-applications")
app.register_blueprint(admin_mentor_bp, url_prefix="/api/admin/mentor")
app.register_blueprint(follow_bp, url_prefix="/api/follows")
app.register_blueprint(comments_bp, url_prefix="/api/comments")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(posts_bp, url_prefix="/api/posts")
app.register_blueprint(resources_bp, url_prefix="/api/resources")
app.register_blueprint(saved_posts_bp, url_prefix="/api/saved-posts")


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
