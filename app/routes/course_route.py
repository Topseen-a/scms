from flask import Blueprint, request, jsonify
from app.services.course_service import CourseService
from app.exceptions.course_exceptions import CourseNotFoundException, InvalidFacilitatorException


course_bp = Blueprint("course_bp", __name__)
course_service = CourseService()


@course_bp.route("/", methods=["POST"])
def create_course():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        result = course_service.create_course(data)
        return jsonify(result), 201
    except InvalidFacilitatorException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@course_bp.route("/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    try:
        result = course_service.get_course_by_id(course_id)
        return jsonify(result), 200
    except CourseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@course_bp.route("/", methods=["GET"])
def get_all_courses():
    try:
        result = course_service.get_all_courses()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@course_bp.route("/facilitator/<int:facilitator_id>", methods=["GET"])
def get_by_facilitator(facilitator_id):
    try:
        result = course_service.get_courses_by_facilitator(facilitator_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@course_bp.route("/<int:course_id>", methods=["PATCH"])
def update_course(course_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        result = course_service.update_course(course_id, data)
        return jsonify(result), 200
    except CourseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except InvalidFacilitatorException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500


@course_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        result = course_service.delete_course(course_id)
        return jsonify(result), 200
    except CourseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal server error","message": str(e)}), 500