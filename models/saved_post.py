# models/saved_post.py
from extensions import db
from datetime import datetime


class SavedPost(db.Model):
    __tablename__ = "saved_posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref="saved_posts", lazy=True)
    post = db.relationship("Post", backref="saved_by", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "createdAt": self.created_at.isoformat(),
            "post": {
                "id": self.post.id,
                "text": self.post.post_text,
                "image": self.post.post_image,
            },
        }
