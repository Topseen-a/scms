from app.database import db
from app.models.course import Course


class CourseRepository:

    def create_course(self, course: Course):
        db.session.add(course)
        db.session.commit()
        return course

    def get_course_by_id(self, course_id: int):
        return db.session.get(Course, course_id)

    def get_all_courses(self):
        return Course.query.all()

    def get_courses_by_facilitator(self, facilitator_id: int):
        return Course.query.filter_by(facilitator_id=facilitator_id).all()

    def update_course(self, course: Course):
        db.session.commit()
        return course

    def delete_course(self, course: Course):
        db.session.delete(course)
        db.session.commit()