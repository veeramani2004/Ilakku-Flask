from extensions import db
from datetime import datetime


class Education(db.Model):
    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True)  # auto-increment or identity
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    school = db.Column(db.String(150), nullable=False)  # required
    degree = db.Column(db.String(150))  # optional
    field_of_study = db.Column(db.String(150))  # optional
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to User
    user = db.relationship("User", back_populates="educations")

    def to_dict(self):
        return {
            "id": self.id,
            "school": self.school,
            "degree": self.degree,
            "fieldOfStudy": self.field_of_study,
            "startYear": self.start_year,
            "endYear": self.end_year,
            "description": self.description,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
