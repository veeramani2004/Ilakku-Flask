from extensions import db
from datetime import datetime
import pytz
from sqlalchemy.dialects.postgresql import JSON

IST = pytz.timezone("Asia/Kolkata")


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)
    related_links = db.Column(JSON, default=list)  # ✅ store as real JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("User", back_populates="resources")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "relatedLinks": self.related_links or [],  # ✅ return list, not string
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "author": {
                "id": self.author.id,
                "name": self.author.name,
                "username": self.author.username,
                "profilePicture": self.author.profile_picture,
            },
        }
