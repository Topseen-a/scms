import re
from app.models.role import Role


class CreateUserRequest:
    def __init__(self, data):
        self.name = data.get("name")
        self.email = data.get("email")
        self.phone_number = data.get("phone_number")
        self.role = data.get("role")

    def validate_user_request(self):
        errors = {}

        if not self.name:
            errors["name"] = "Name is required"
        if not self.email:
            errors["email"] = "Email is required"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors["email"] = "Invalid email format"
        if not self.phone_number:
            errors["phone_number"] = "Phone number is required"
        elif len(self.phone_number) != 11:
            errors["phone_number"] = "Phone number must be 11 digits"
        if not self.role:
            errors["role"] = "Role is required"
        elif self.role.upper() not in [role.value for role in Role]:
            errors["role"] = "Invalid role"

        return errors

class CreateUserResponse:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.role = user.role.value if user.role else None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
        }