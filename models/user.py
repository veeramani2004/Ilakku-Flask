from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    about = db.Column(db.Text)
    bio = db.Column(db.String(255))
    profile_picture = db.Column(db.Text)
    poster = db.Column(db.Text)
    positions = db.Column(db.String(100))
    role = db.Column(db.String(20), nullable=False, default="USER")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Relationships
    posts = db.relationship("Post", back_populates="author")
    educations = db.relationship(
        "Education", back_populates="user", cascade="all, delete-orphan"
    )
    experiences = db.relationship(
        "Experience", back_populates="user", cascade="all, delete-orphan"
    )
    resources = db.relationship(
        "Resource", back_populates="author", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "city": self.city,
            "country": self.country,
            "industry": self.industry,
            "bio": self.bio,
            "about": self.about,
            "profilePicture": self.profile_picture,
            "poster": self.poster,
            "positions": self.positions,
            "role": self.role,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            # ✅ include related data
            "educations": [edu.to_dict() for edu in self.educations],
            "experiences": [exp.to_dict() for exp in self.experiences],
        }
