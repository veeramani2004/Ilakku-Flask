from extensions import db
from datetime import datetime


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    company = db.Column(db.String(150), nullable=False)  # required
    title = db.Column(db.String(150))
    employment_type = db.Column(db.String(50))  # e.g. Full-time, Intern
    location = db.Column(db.String(150))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)  # NULL if current
    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to User
    user = db.relationship("User", back_populates="experiences")

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "title": self.title,
            "employmentType": self.employment_type,
            "location": self.location,
            "startDate": self.start_date.isoformat() if self.start_date else None,
            "endDate": self.end_date.isoformat() if self.end_date else None,
            "description": self.description,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
