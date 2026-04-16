class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        self.status_code = 404
        super().__init__(message)

class InvalidUserRoleException(Exception):
    def __init__(self, message="Invalid user role provided"):
        self.message = message
        self.status_code = 400
        super().__init__(message)

class EmailAlreadyExistsException(Exception):
    def __init__(self, message="Email already exists"):
        self.message = message
        self.status_code = 409
        super().__init__(message)