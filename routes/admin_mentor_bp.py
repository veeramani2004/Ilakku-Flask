# routes/admin_mentor_bp.py
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from extensions import db
from models.user import User
from models.mentor_application import MentorApplication

admin_mentor_bp = Blueprint("admin_mentor_bp", __name__)


# 🔒 Decorator to allow only Admins
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            return jsonify({"error": "Authentication required"}), 401

        # ✅ Use username instead of id
        user = User.query.filter_by(username=identity).first()
        if not user or user.role != "ADMIN":
            return jsonify({"error": "Admins only"}), 403

        return fn(*args, **kwargs)

    return wrapper


# 👀 Get all mentor applications (Admins only)
@admin_mentor_bp.get("/applications")
@jwt_required()
@admin_required
def get_applications():
    apps = MentorApplication.query.order_by(MentorApplication.created_at.desc()).all()
    return jsonify([a.to_dict() for a in apps]), 200


# ✅ Approve mentor application (Admins only)
@admin_mentor_bp.put("/applications/<int:app_id>/approve")
@jwt_required()
@admin_required
def approve_application(app_id):
    application = MentorApplication.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    user = User.query.get(application.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    application.status = "APPROVED"
    user.role = "MENTOR"
    db.session.commit()

    return jsonify({"message": "Application approved", "user_role": user.role}), 200


# ❌ Reject mentor application (Admins only)
@admin_mentor_bp.put("/applications/<int:app_id>/reject")
@jwt_required()
@admin_required
def reject_application(app_id):
    application = MentorApplication.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    application.status = "REJECTED"
    db.session.commit()

    return jsonify({"message": "Application rejected"}), 200
