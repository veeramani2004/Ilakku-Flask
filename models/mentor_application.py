# models/mentor_application.py
from extensions import db
from datetime import datetime


class MentorApplication(db.Model):
    __tablename__ = "mentor_applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Personal & Identity
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    # Professional Info
    job_title = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)

    office_address_line1 = db.Column(db.String(255), nullable=True)
    office_city = db.Column(db.String(100), nullable=True)
    office_state_country = db.Column(db.String(120), nullable=True)
    office_contact = db.Column(db.String(20), nullable=True)

    # Professional Validation
    linkedin_url = db.Column(db.String(255), nullable=False)
    years_experience = db.Column(
        db.String(20), nullable=False
    )  # e.g., "1-2", "3-5", etc.

    # Motivation
    motivation = db.Column(db.Text, nullable=True)

    # Application status
    status = db.Column(db.String(20), default="PENDING")
    # can be "PENDING", "APPROVED", "REJECTED"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship("User", backref="mentor_applications")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "job_title": self.job_title,
            "company_name": self.company_name,
            "office_address_line1": self.office_address_line1,
            "office_city": self.office_city,
            "office_state_country": self.office_state_country,
            "office_contact": self.office_contact,
            "linkedin_url": self.linkedin_url,
            "years_experience": self.years_experience,
            "motivation": self.motivation,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
