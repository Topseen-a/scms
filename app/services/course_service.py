from app.exceptions.course_exceptions import InvalidFacilitatorException, CourseNotFoundException
from app.models.course import Course
from app.models.role import Role
from app.repositories.course_repository import CourseRepository
from app.repositories.user_repository import UserRepository
from app.schemas.course_schema import CreateCourseRequest, CreateCourseResponse


class CourseService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.user_repo = UserRepository()

    def create_course(self, data):
        request = CreateCourseRequest(data)
        errors = request.validate_course_request()
        if errors:
            return {"errors": errors}

        facilitator = self.user_repo.get_user_by_id(request.facilitator_id)

        if not facilitator:
            raise InvalidFacilitatorException()
        if not facilitator.role != Role.FACILITATOR:
            return {"errors": "User is not a facilitator"}

        course = Course(
            title=request.title,
            description=request.description,
            code=request.code,
            facilitator_id=request.facilitator_id
        )

        saved_course = self.course_repo.create_course(course)
        return CreateCourseResponse(saved_course).to_dict()

    def get_course_by_id(self, course_id: int):
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise CourseNotFoundException()

        return CreateCourseResponse(course).to_dict()

    def get_all_courses(self):
        courses = self.course_repo.get_all_courses()
        return [CreateCourseResponse(course).to_dict() for course in courses]

    def get_courses_by_facilitator_id(self, facilitator_id: int):
        courses = self.course_repo.get_courses_by_facilitator(facilitator_id)
        return [CreateCourseResponse(course).to_dict() for course in courses]

    def update_course(self, course: Course, data):
        course = self.course_repo.get_course_by_id(course.id)
        if not course:
            raise CourseNotFoundException()
        if "title" in data:
            course.title = data["title"]
        if "description" in data:
            course.description = data["description"]
        if "code" in data:
            course.code = data["code"]
        if "facilitator_id" in data:
            course.facilitator_id = data["facilitator_id"]

        updated_course = self.course_repo.update_course(course)
        return CreateCourseResponse(updated_course).to_dict()

    def delete_course(self, course_id: int):
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise CourseNotFoundException()

        self.course_repo.delete_course(course)
        return {"message": "Course deleted successfully"}