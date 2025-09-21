from flask import Blueprint, request, jsonify
from extensions import db
from models.saved_post import SavedPost
from models.post import Post
from models.user import User

saved_posts_bp = Blueprint("saved_posts_bp", __name__)


# ➕ Save a post
@saved_posts_bp.post("/")
def save_post():
    data = request.get_json()
    user_id = data.get("user_id")
    post_id = data.get("post_id")

    if not user_id or not post_id:
        return jsonify({"error": "Missing fields"}), 400

    # check if already saved
    existing = SavedPost.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing:
        return jsonify({"message": "Already saved"}), 200

    saved = SavedPost(user_id=user_id, post_id=post_id)
    db.session.add(saved)
    db.session.commit()
    return jsonify(saved.to_dict()), 201


@saved_posts_bp.delete("/<int:post_id>/<int:user_id>")
def unsave_post(post_id, user_id):
    saved = SavedPost.query.filter_by(user_id=user_id, post_id=post_id).first()
    if saved:
        db.session.delete(saved)
        db.session.commit()
        return jsonify({"message": "Post unsaved"}), 200

    # still return success (no-op)
    return jsonify({"message": "Already unsaved"}), 200


# 📥 Get saved posts for a user
@saved_posts_bp.get("/user/<int:user_id>")
def get_saved_posts(user_id):
    saved = SavedPost.query.filter_by(user_id=user_id).all()
    return jsonify(
        [{**s.to_dict(), "post": s.post.to_dict() if s.post else None} for s in saved]
    ), 200
