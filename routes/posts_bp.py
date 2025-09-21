from flask import Blueprint, request, jsonify
from extensions import db
from models.post import Post
from models.user import User

posts_bp = Blueprint("posts_bp", __name__)


# CREATE post
@posts_bp.post("")
@posts_bp.post("/")
def create_post():
    data = request.get_json()
    post = Post(
        user_id=data.get("user_id"),
        post_text=data.get("post_text"),
        post_image=data.get("post_image"),
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


# GET all posts (joined with users)
@posts_bp.get("")
@posts_bp.get("/")
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])


# ✅ GET posts by specific user
@posts_bp.get("/user/<int:user_id>")
def get_posts_by_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


# UPDATE post
@posts_bp.put("/<int:post_id>")
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    post.post_text = data.get("post_text", post.post_text)
    post.post_image = data.get("post_image", post.post_image)

    try:
        db.session.commit()
        db.session.refresh(post)  # ✅ refresh so relationships load safely
        return jsonify(post.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE post
@posts_bp.delete("/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})



# 📥 Get a single post by ID
@posts_bp.get("/<int:post_id>")
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post.to_dict()), 200
