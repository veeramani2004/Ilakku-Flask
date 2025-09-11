from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), nullable=False, default="USER")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        # Frontend JSON key - Backend Value mapping
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "profilePicture": self.profile_picture,
            "role": self.role,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "password": self.password,
        }
