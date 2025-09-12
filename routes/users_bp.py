from flask import Blueprint, request
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

HTTP_NOT_FOUND = 404
HTTP_CREATED = 201
HTTP_ERROR = 500

users_bp = Blueprint("users_bp", __name__)


@users_bp.post("/signup")
def create_user():
    data = request.get_json()

    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    profile_picture = data.get("profile_picture") or data.get("profilePicture")

    if not name or not username or not email or not password:
        return {"error": "name, username, email, and password are required"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "username already taken"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "email already registered"}, 400

    hashed_password = generate_password_hash(password)

    if not profile_picture:
        profile_picture = "https://example.com/default-avatar.png"

    new_user = User(
        name=name,
        username=username,
        email=email,
        password=hashed_password,
        profile_picture=profile_picture,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Sign Up Successful"}, HTTP_CREATED
    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_ERROR


@users_bp.post("/login")
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username / password required"}, 400

    db_user = User.query.filter_by(username=username).first()

    if not db_user:
        return {"error": "username or password is incorrect"}, 401

    if not check_password_hash(db_user.password, password):
        return {"error": "username or password is incorrect"}, 401

    token = create_access_token(identity=username)

    return {
        "message": "Login Successful",
        "token": token,
        "username": db_user.username,
        "role": db_user.role,
    }, 200


@users_bp.get("/user/<string:username>")
@jwt_required()
def get_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {"error": "User not found"}, 404

    return user.to_dict(), 200
