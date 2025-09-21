from flask import Blueprint, request, jsonify
from extensions import db
from models.resource import Resource
from models.user import User
import json

resources_bp = Blueprint("resources_bp", __name__)


@resources_bp.post("")
@resources_bp.post("/")
def create_resource():
    try:
        data = request.get_json()

        raw_links = data.get("related_links")

        # 🔹 Always normalize to a list
        if isinstance(raw_links, str):
            try:
                # if frontend accidentally sends JSON string, parse it
                parsed = json.loads(raw_links)
                related_links = parsed if isinstance(parsed, list) else [parsed]
            except json.JSONDecodeError:
                related_links = [raw_links] if raw_links.strip() else []
        elif isinstance(raw_links, list):
            related_links = raw_links
        else:
            related_links = []

        resource = Resource(
            user_id=data.get("user_id"),
            title=data.get("title"),
            description=data.get("description"),
            content=data.get("content"),
            related_links=related_links,  # ✅ real list, not string
        )
        db.session.add(resource)
        db.session.commit()
        return jsonify(resource.to_dict()), 201

    except Exception as e:
        import traceback

        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Get all resources
@resources_bp.get("")
@resources_bp.get("/")
def get_resources():
    resources = Resource.query.order_by(Resource.created_at.desc()).all()
    return jsonify([r.to_dict() for r in resources]), 200


# Get single resource (full blog)
@resources_bp.get("/<int:resource_id>")
def get_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify(resource.to_dict()), 200


# Get resources by user
@resources_bp.get("/user/<int:user_id>")
def get_resources_by_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    resources = (
        Resource.query.filter_by(user_id=user_id)
        .order_by(Resource.created_at.desc())
        .all()
    )
    return jsonify([r.to_dict() for r in resources]), 200


# Update resource
@resources_bp.put("/<int:resource_id>")
def update_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    data = request.get_json()
    resource.title = data.get("title", resource.title)
    resource.description = data.get("description", resource.description)
    resource.content = data.get("content", resource.content)

    # ✅ Handle both frontend styles (camelCase or snake_case)
    links = data.get("related_links") or data.get("relatedLinks")
    if isinstance(links, list):
        resource.related_links = links
    elif isinstance(links, str):
        try:
            resource.related_links = json.loads(links)
        except Exception:
            resource.related_links = [links] if links.strip() else []

    try:
        db.session.commit()
        return jsonify(resource.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Delete resource
@resources_bp.delete("/<int:resource_id>")
def delete_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted"}), 200
