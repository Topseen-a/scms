import re


class CreateCourseRequest:
    def __init__(self, data):
        self.title = data.get("title")
        self.description = data.get("description")
        self.code = data.get("code")
        self.facilitator_id = data.get("facilitator_id")

    def validate_course_request(self):
        errors = {}

        if not self.title:
            errors["title"] = "Title is required"
        if not self.description:
            errors["description"] = "Description is required"
        if not self.code:
            errors["code"] = "Course code is required"
        elif not re.match(r"^[A-Z]{2,10}[0-9]{1,5}$", self.code):
            errors["code"] = "Invalid course code format (e.g. CSC101)"
        if not self.facilitator_id:
            errors["facilitator_id"] = "Facilitator ID is required"

        return errors


class CreateCourseResponse:
    def __init__(self, course):
        self.id = course.id
        self.title = course.title
        self.description = course.description
        self.code = course.code
        self.facilitator_id = course.facilitator_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "code": self.code,
            "facilitator_id": self.facilitator_id
        }