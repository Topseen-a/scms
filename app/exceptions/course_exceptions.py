class CourseNotFoundException(Exception):
    def __init__(self, message="Course not found"):
        self.message = message
        self.status_code = 404
        super().__init__(message)

class InvalidFacilitatorException(Exception):
    def __init__(self, message="Invalid facilitator"):
        self.message = message
        self.status_code = 400
        super().__init__(message)