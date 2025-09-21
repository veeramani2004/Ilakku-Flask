# routes/comments_bp.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.comment import Comment
from models.user import User
from models.post import Post

comments_bp = Blueprint("comments_bp", __name__)


# ➕ Add a comment to a post
@comments_bp.post("")
@comments_bp.post("/")
def add_comment():
    data = request.get_json()
    user_id = data.get("user_id")
    post_id = data.get("post_id")
    content = data.get("content")

    if not user_id or not post_id or not content:
        return jsonify({"error": "Missing fields"}), 400

    comment = Comment(user_id=user_id, post_id=post_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201


# 📥 Get comments for a post
@comments_bp.get("/post/<int:post_id>")
def get_post_comments(post_id):
    comments = (
        Comment.query.filter_by(post_id=post_id)
        .order_by(Comment.created_at.desc())
        .all()
    )
    return jsonify([c.to_dict() for c in comments]), 200


# ✏️ Update a comment
@comments_bp.put("/<int:comment_id>")
def update_comment(comment_id):
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Content required"}), 400

    comment = Comment.query.get_or_404(comment_id)
    comment.content = content
    db.session.commit()
    return jsonify(comment.to_dict()), 200


# 🗑 Delete a comment
@comments_bp.delete("/<int:comment_id>")
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200
