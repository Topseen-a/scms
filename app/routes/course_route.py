from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.services.course_service import CourseService
from app.schemas.course_schema import CourseCreate
from app.exceptions.course_exceptions import (
    CourseNotFoundException,
    InvalidFacilitatorException
)

course_bp = Blueprint("courses", __name__, url_prefix="/api/courses")
course_service = CourseService()


@course_bp.route("/", methods=["POST"])
def create_course():
    try:
        data = request.get_json()
        course = CourseCreate(**data)

        result = course_service.create_course(course)
        return jsonify(result), 201

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    except InvalidFacilitatorException as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500


@course_bp.route("/<course_id>", methods=["GET"])
def get_course(course_id):
    try:
        result = course_service.get_course_by_id(course_id)
        return jsonify(result), 200

    except CourseNotFoundException as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500


@course_bp.route("/", methods=["GET"])
def get_all_courses():
    try:
        result = course_service.get_all_courses()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500


@course_bp.route("/facilitator/<facilitator_id>", methods=["GET"])
def get_by_facilitator(facilitator_id):
    try:
        result = course_service.get_courses_by_facilitator(facilitator_id)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500


@course_bp.route("/<course_id>", methods=["PATCH"])
def update_course(course_id):
    try:
        data = request.get_json()
        result = course_service.update_course(course_id, data)
        return jsonify(result), 200

    except CourseNotFoundException as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500


@course_bp.route("/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        result = course_service.delete_course(course_id)
        return jsonify(result), 200

    except CourseNotFoundException as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error",
                        "message": str(e)}), 500