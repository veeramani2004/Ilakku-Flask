# routes/follow_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.follow import Follow
from models.user import User

follow_bp = Blueprint("follow_bp", __name__)


# ➕ Follow a user (expects JSON body)
@follow_bp.post("/")
def follow_user():
    data = request.get_json()
    follower_id = data.get("follower_id")
    following_id = data.get("following_id")

    if not follower_id or not following_id:
        return jsonify({"error": "Missing fields"}), 400

    if follower_id == following_id:
        return jsonify({"error": "You cannot follow yourself"}), 400

    existing = Follow.query.filter_by(
        follower_id=follower_id, following_id=following_id
    ).first()

    if existing:
        return jsonify({"message": "Already following"}), 200

    follow = Follow(follower_id=follower_id, following_id=following_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify(follow.to_dict()), 201


# ❌ Unfollow a user
@follow_bp.delete("/<int:follower_id>/<int:following_id>")
def unfollow_user(follower_id, following_id):
    follow = Follow.query.filter_by(
        follower_id=follower_id, following_id=following_id
    ).first()
    if not follow:
        return jsonify({"error": "Not following"}), 404

    db.session.delete(follow)
    db.session.commit()
    return jsonify({"message": "Unfollowed"}), 200


# 👥 Get followers of a user
@follow_bp.get("/followers/<int:user_id>")
def get_followers(user_id):
    followers = Follow.query.filter_by(following_id=user_id).all()
    return jsonify([f.to_dict() for f in followers]), 200


# 👤 Get who a user follows
@follow_bp.get("/following/<int:user_id>")
def get_following(user_id):
    following = Follow.query.filter_by(follower_id=user_id).all()
    return jsonify([f.to_dict() for f in following]), 200


# ✅ Check follow status (for PostCard button)
@follow_bp.get("/status/<int:follower_id>/<int:following_id>")
def check_follow_status(follower_id, following_id):
    if follower_id == following_id:
        return jsonify({"is_following": False}), 200  # can't follow yourself

    existing = Follow.query.filter_by(
        follower_id=follower_id, following_id=following_id
    ).first()

    return jsonify({"is_following": existing is not None}), 200
