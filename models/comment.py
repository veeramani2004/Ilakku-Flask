# models/comment.py
from extensions import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Relationships
    user = db.relationship("User", backref="comments")
    post = db.relationship("Post", backref="comments", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "createdAt": self.created_at.isoformat(),
            "author": {
                "id": self.user.id,
                "name": self.user.username,
                "profilePicture": self.user.profile_picture,
            },
        }
