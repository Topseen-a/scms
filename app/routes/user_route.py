from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.exceptions.user_exceptions import UserNotFoundException, InvalidUserRoleException, EmailAlreadyExistsException


user_bp = Blueprint("user_bp", __name__)
user_service = UserService()


@user_bp.route("/", methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        result = user_service.register_user(data)
        return jsonify(result), 201
    except (InvalidUserRoleException, EmailAlreadyExistsException) as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        result = user_service.get_user_by_id(user_id)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@user_bp.route("/email/<string:email>", methods=["GET"])
def get_user_by_email(email):
    try:
        result = user_service.get_user_by_email(email)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@user_bp.route("/", methods=["GET"])
def get_all_users():
    try:
        result = user_service.get_all_users()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        result = user_service.update_user(user_id, data)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except (InvalidUserRoleException, EmailAlreadyExistsException) as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = user_service.delete_user(user_id)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:return jsonify({"error": "Internal server error","message": str(e)}), 500