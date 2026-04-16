from app.exceptions.user_exceptions import EmailAlreadyExistsException, UserNotFoundException, InvalidUserRoleException
from app.models.user import User, Role
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserRequest, CreateUserResponse


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, data):
        request = CreateUserRequest(data)
        errors = request.validate_user_request()
        if errors:
            return {"errors": errors}

        existing_user = self.user_repo.get_user_by_email(request.email)
        if existing_user:
            raise EmailAlreadyExistsException()

        role = Role(request.role.upper())

        user = User(
            name=request.name,
            email=request.email,
            role=role,
            phone_number=request.phone_number
        )

        saved_user = self.user_repo.create_user(user)
        return CreateUserResponse(saved_user).to_dict()

    def get_user_by_id(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        return CreateUserResponse(user).to_dict()

    def get_user_by_email(self, email: str):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundException()

        return CreateUserResponse(user).to_dict(), 200

    def get_all_users(self):
        users = self.user_repo.get_all_users()
        return [CreateUserResponse(user).to_dict() for user in users], 200

    def update_user(self, user_id: int, data):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}, 404
        if "email" in data:
            existing_user = self.user_repo.get_user_by_email(data["email"])
            if existing_user and existing_user.id != user.id:
                raise EmailAlreadyExistsException()
            user.email = data["email"]
        if "name" in data:
            user.name = data["name"]
        if "phone_number" in data:
            user.phone_number = data["phone_number"]
        if "role" in data:
            try:
                user.role = Role(data["role"].upper())
            except Exception:
                raise InvalidUserRoleException()

        updated_user = self.user_repo.update_user(user)
        return CreateUserResponse(updated_user).to_dict()

    def delete_user(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        self.user_repo.delete_user(user)
        return {"message": "User deleted successfully"}