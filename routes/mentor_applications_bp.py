# routes/mentor_applications_bp.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from extensions import db
from models.mentor_application import MentorApplication

mentor_app_bp = Blueprint("mentor_app_bp", __name__)


# 📝 Apply to become a mentor (USER)

@mentor_app_bp.post("/")
@jwt_required()
def apply_mentor():
    identity = get_jwt_identity()
    data = request.get_json()

    # Prevent duplicate pending applications
    existing = MentorApplication.query.filter_by(
        user_id=identity, status="PENDING"
    ).first()
    if existing:
        return jsonify({"error": "You already have a pending application"}), 400

    application = MentorApplication(
        user_id=identity,
        full_name=data.get("full_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        job_title=data.get("job_title"),
        company_name=data.get("company_name"),
        office_address_line1=data.get("office_address_line1"),
        office_city=data.get("office_city"),
        office_state_country=data.get("office_state_country"),
        office_contact=data.get("office_contact"),
        linkedin_url=data.get("linkedin_url"),
        years_experience=data.get("years_experience"),
        motivation=data.get("motivation"),
        status="PENDING",
    )

    db.session.add(application)
    db.session.commit()

    return jsonify(
        {"message": "Application submitted", "application": application.to_dict()}
    ), 201


# 👀 Get my own applications (USER)
@mentor_app_bp.get("/my-applications")
@jwt_required()
def get_my_applications():
    identity = get_jwt_identity()
    apps = (
        MentorApplication.query.filter_by(user_id=identity)
        .order_by(MentorApplication.created_at.desc())
        .all()
    )
    return jsonify([a.to_dict() for a in apps]), 200
