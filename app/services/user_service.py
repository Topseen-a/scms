from app.models.user import User, Role
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserRequest, CreateUserResponse
from app.exceptions.user_exceptions import UserNotFoundException, InvalidUserRoleException


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository


    def register_user(self, data):
        request = CreateUserRequest(data)
        errors = request.validate_user_request()
        if errors:
            return {"errors": errors}

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

        return CreateUserResponse(user).to_dict()


    def get_all_users(self):
        users = self.user_repo.get_all_users()
        return [CreateUserResponse(user).to_dict() for user in users]


    def update_user(self, user_id: int, data):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "role" in data:
            user.role = Role(data["role"].upper())
        if "phone_number" in data:
            user.phone_number = data["phone_number"]

        updated_user = self.user_repo.update_user(user)
        return CreateUserResponse(updated_user).to_dict()


    def delete_user(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        self.user_repo.delete_user(user)
        return{"message": "User deleted successfully"}