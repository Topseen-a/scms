from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    InvalidUserRoleException
)

user_bp = Blueprint("users", __name__, url_prefix="/api/users")
user_service = UserService()

@user_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user = UserCreate(**data)
        result = user_service.create_user(user)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": "Validation error",
                        "details": e.errors()}), 400
    except InvalidUserRoleException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500


@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        result = user_service.get_user_by_id(user_id)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@user_bp.route("/", methods=["GET"])
def get_all_users():
    try:
        result = user_service.get_all_users()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@user_bp.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        data = request.get_json()
        result = user_service.update_user(user_id, data)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = user_service.delete_user(user_id)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500