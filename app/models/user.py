from app.database import db
from app.models.role import Role


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    courses = db.relationship("Course", backref="facilitator", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role.value if self.role else None,
        }