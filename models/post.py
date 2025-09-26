from extensions import db
import pytz
from datetime import datetime

# Define IST timezone
IST = pytz.timezone("Asia/Kolkata")


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_text = db.Column(db.Text)
    post_image = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(IST)
    )  # store in IST

    author = db.relationship("User", back_populates="posts")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "postText": self.post_text,
            "postImage": self.post_image,
            # ✅ return with IST offset (+05:30)
            "createdAt": self.created_at.astimezone(IST).isoformat()
            if self.created_at
            else None,
            "author": {
                "id": self.author.id,
                "username": self.author.username,
                "name": self.author.name,
                "bio": self.author.bio,
                "profilePicture": self.author.profile_picture,
                "positions": self.author.positions,
                "role": self.author.role,
            },
        }
