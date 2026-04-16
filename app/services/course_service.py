from app.repositories.course_repository import CourseRepository
from app.repositories.user_repository import UserRepository
from app.models.course import Course
from app.schemas.course_schema import CourseCreate
from app.exceptions.course_exceptions import (
    CourseNotFoundException,
    InvalidFacilitatorException
)


class CourseService:

    def __init__(self):
        self.course_repository = CourseRepository()
        self.user_repository = UserRepository()

    def create_course(self, course: CourseCreate):
        facilitator = self.user_repository.get_user_by_id(course.facilitator_id)

        if not facilitator:
            raise InvalidFacilitatorException("Facilitator not found")

        if facilitator["role"] != "facilitator":
            raise InvalidFacilitatorException("User is not a facilitator")

        course_data = course.model_dump()
        course_model = Course(**course_data)
        result = self.course_repository.create_course(
            course_model.to_dict()
        )

        course_model.id = str(result.inserted_id)
        return self._format_response(course_model)

    def get_course_by_id(self, course_id: str):
        course = self.course_repository.get_course_by_id(course_id)

        if not course:
            raise CourseNotFoundException("Course not found")

        return self._format_response(Course.from_dict(course))

    def get_all_courses(self):
        courses = self.course_repository.get_all_courses()

        return [
            self._format_response(Course.from_dict(course))
            for course in courses
        ]

    def get_courses_by_facilitator(self, facilitator_id: str):
        courses = self.course_repository.get_courses_by_facilitator(facilitator_id)

        return [
            self._format_response(Course.from_dict(course))
            for course in courses
        ]

    def update_course(self, course_id: str, update_data: dict):
        result = self.course_repository.update_course(course_id, update_data)

        if result.modified_count == 0:
            raise CourseNotFoundException("Course not found")

        return {"message": "Course updated successfully"}

    def delete_course(self, course_id: str):
        result = self.course_repository.delete_course(course_id)

        if result.deleted_count == 0:
            raise CourseNotFoundException("Course not found")

        return {"message": "Course deleted successfully"}

    def _format_response(self, course: Course):
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "code": course.code,
            "facilitator_id": course.facilitator_id
        }