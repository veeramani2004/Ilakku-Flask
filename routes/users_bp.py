from flask import Blueprint, request
from models.user import User
from models.education import Education
from models.experience import Experience
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

HTTP_NOT_FOUND = 404
HTTP_CREATED = 201
HTTP_ERROR = 500

users_bp = Blueprint("users_bp", __name__)


# -------------------------
# SIGNUP
# -------------------------
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

    # hashed_password = generate_password_hash(password)
    hashed_password = password

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


# -------------------------
# LOGIN
# -------------------------
@users_bp.post("/login")
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username / password required"}, 400

    db_user = User.query.filter_by(username=username).first()

    # if not db_user or not check_password_hash(db_user.password, password):
    #     return {"error": "username or password is incorrect"}, 401
    if not db_user or not (db_user.password, password):
        return {"error": "username or password is incorrect"}, 401
    token = create_access_token(identity=username)

    return {
        "message": "Login Successful",
        "token": token,
        "id": db_user.id,
        "username": db_user.username,
        "role": db_user.role,
    }, 200


# -------------------------
# GET USER PROFILE
# -------------------------
@users_bp.get("/<string:username>")
@jwt_required()
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return {"user": user.to_dict()}, 200


# -------------------------
# UPDATE USER PROFILE
# -------------------------
@users_bp.put("/<string:username>")
@jwt_required()
def update_user(username):
    user = User.query.filter_by(username=username).first_or_404()

    data = request.get_json()

    user.name = data.get("name", user.name)
    user.positions = data.get("positions", user.positions)
    user.poster = data.get("poster", user.poster)
    user.bio = data.get("bio", user.bio)
    user.about = data.get("about", user.about)
    user.city = data.get("city", user.city)
    user.country = data.get("country", user.country)
    user.industry = data.get("industry", user.industry)
    user.profile_picture = data.get("profilePicture", user.profile_picture)

    try:
        db.session.commit()
        return {"message": "Profile updated successfully", "user": user.to_dict()}, 200
    except Exception as err:
        db.session.rollback()
        return {"error": str(err)}, HTTP_ERROR


# -------------------------
# EDUCATION ROUTES
# -------------------------
@users_bp.get("/<int:user_id>/educations")
@jwt_required()
def get_user_educations(user_id):
    user = User.query.get_or_404(user_id)
    return {"educations": [edu.to_dict() for edu in user.educations]}, 200


@users_bp.post("/<int:user_id>/educations")
@jwt_required()
def add_user_education(user_id):
    data = request.get_json()
    if not data.get("school"):
        return {"error": "School name is required"}, 400

    new_edu = Education(
        user_id=user_id,
        school=data.get("school"),
        degree=data.get("degree"),
        field_of_study=data.get("fieldOfStudy"),
        start_year=data.get("startYear"),
        end_year=data.get("endYear"),
        description=data.get("description"),
    )
    db.session.add(new_edu)
    db.session.commit()
    return {"message": "Education added", "education": new_edu.to_dict()}, HTTP_CREATED


@users_bp.put("/educations/<int:edu_id>")
@jwt_required()
def update_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    data = request.get_json()

    edu.school = data.get("school", edu.school)
    edu.degree = data.get("degree", edu.degree)
    edu.field_of_study = data.get("fieldOfStudy", edu.field_of_study)
    edu.start_year = data.get("startYear", edu.start_year)
    edu.end_year = data.get("endYear", edu.end_year)
    edu.description = data.get("description", edu.description)

    db.session.commit()
    return {"message": "Education updated", "education": edu.to_dict()}, 200


@users_bp.delete("/educations/<int:edu_id>")
@jwt_required()
def delete_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    db.session.delete(edu)
    db.session.commit()
    return {"message": "Education deleted"}, 200


# -------------------------
# EXPERIENCE ROUTES
# -------------------------
@users_bp.get("/<int:user_id>/experiences")
@jwt_required()
def get_user_experiences(user_id):
    user = User.query.get_or_404(user_id)
    return {"experiences": [exp.to_dict() for exp in user.experiences]}, 200


@users_bp.post("/<int:user_id>/experiences")
@jwt_required()
def add_user_experience(user_id):
    data = request.get_json()
    if not data.get("company"):
        return {"error": "Company name is required"}, 400

    new_exp = Experience(
        user_id=user_id,
        company=data.get("company"),
        title=data.get("title"),
        employment_type=data.get("employmentType"),
        location=data.get("location"),
        start_date=data.get("startDate"),
        end_date=data.get("endDate"),
        description=data.get("description"),
    )
    db.session.add(new_exp)
    db.session.commit()
    return {
        "message": "Experience added",
        "experience": new_exp.to_dict(),
    }, HTTP_CREATED


@users_bp.put("/experiences/<int:exp_id>")
@jwt_required()
def update_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    data = request.get_json()

    exp.company = data.get("company", exp.company)
    exp.title = data.get("title", exp.title)
    exp.employment_type = data.get("employmentType", exp.employment_type)
    exp.location = data.get("location", exp.location)
    exp.start_date = data.get("startDate", exp.start_date)
    exp.end_date = data.get("endDate", exp.end_date)
    exp.description = data.get("description", exp.description)

    db.session.commit()
    return {"message": "Experience updated", "experience": exp.to_dict()}, 200


@users_bp.delete("/experiences/<int:exp_id>")
@jwt_required()
def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()
    return {"message": "Experience deleted"}, 200
