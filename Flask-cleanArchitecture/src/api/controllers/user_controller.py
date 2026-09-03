from flask import Blueprint, jsonify, request

from api.schemas.user import (
    UserResponseSchema,
    UserUpdateRequestSchema
)

from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository


user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/users"
)


user_service = UserService(
    UserRepository()
)

user_response_schema = UserResponseSchema()
user_update_schema = UserUpdateRequestSchema()


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = user_service.get_by_id(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    result = {
        "id": user.ID,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "avatar": user.avatar,
        "created_at": user.created_at,
        "status": user.status,
        "role_id": user.role_id
    }

    return jsonify(
        user_response_schema.dump(result)
    ), 200


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = user_update_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:

        user = user_service.update(
            user_id,
            data
        )

        result = {
            "id": user.ID,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "avatar": user.avatar,
            "created_at": user.created_at,
            "status": user.status,
            "role_id": user.role_id
        }

        return jsonify(
            user_response_schema.dump(result)
        ), 200

    except ValueError as e:

        return jsonify({
            "message": str(e)
        }), 404

    except Exception as e:

        return jsonify({
            "message": "Update profile failed",
            "error": str(e)
        }), 500