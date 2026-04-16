from app.database import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    facilitator_id = db.Column(db.Integer, db.ForeignKey('facilitators.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "code": self.code,
            "facilitator_id": self.facilitator_id
        }