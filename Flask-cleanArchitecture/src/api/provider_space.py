"""Provider-only APIs for managing creative spaces.

This module is intentionally self-contained so it can be reviewed and
registered without changing the public Creative Space controller.
"""

from functools import wraps

import jwt
from flask import Blueprint, current_app, g, jsonify, request

from api.schemas.creative_space import (
    CreativeSpaceRequestSchema,
    CreativeSpaceResponseSchema,
)
from infrastructure.databases.postgres import session
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.repositories.creative_space_repository import (
    CreativeSpaceRepository,
)
from infrastructure.repositories.service_provider_repository import (
    ServiceProviderRepository,
)
from services.creative_space_service import CreativeSpaceService


bp = Blueprint(
    "provider_space",
    __name__,
    url_prefix="/provider/spaces",
)

space_service = CreativeSpaceService(
    CreativeSpaceRepository(session),
    ServiceProviderRepository(session),
)
request_schema = CreativeSpaceRequestSchema()
response_schema = CreativeSpaceResponseSchema()

ALLOWED_STATUSES = {"active", "inactive"}


def provider_required(view):
    """Require a valid Service Provider JWT for a view."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            return jsonify({"message": "Authentication is required"}), 401

        try:
            payload = jwt.decode(
                authorization[7:].strip(),
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        try:
            role_id = int(payload.get("role_id"))
            provider_id = int(payload.get("provider_id"))
        except (TypeError, ValueError):
            return jsonify({"message": "Provider access is required"}), 403

        if role_id != 3 or provider_id <= 0:
            return jsonify({"message": "Provider access is required"}), 403

        g.provider_id = provider_id
        return view(*args, **kwargs)

    return wrapped


def _owned_space(space_id):
    return session.query(CreativeSpaceModel).filter(
        CreativeSpaceModel.id == space_id,
        CreativeSpaceModel.provider_id == g.provider_id,
    ).first()


def _validate_business_rules(data):
    if data.get("status") not in ALLOWED_STATUSES:
        return "Status must be active or inactive"

    for field in ("max_capacity", "base_price"):
        try:
            if float(data.get(field)) <= 0:
                return f"{field} must be greater than 0"
        except (TypeError, ValueError):
            return f"{field} must be a valid number"

    if data.get("size_sqm") is not None:
        try:
            if float(data["size_sqm"]) <= 0:
                return "size_sqm must be greater than 0"
        except (TypeError, ValueError):
            return "size_sqm must be a valid number"

    return None


@bp.get("")
@bp.get("/")
@provider_required
def list_spaces():
    items = space_service.list_spaces(provider_id=g.provider_id)
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.get("/<int:space_id>")
@provider_required
def get_space(space_id):
    if not _owned_space(space_id):
        return jsonify({"message": "Space not found"}), 404

    item = space_service.get_space_detail(space_id)
    return jsonify(response_schema.dump(item)), 200


@bp.post("")
@bp.post("/")
@provider_required
def create_space():
    data = request.get_json(silent=True) or {}
    data.pop("provider_id", None)
    data["provider_id"] = g.provider_id

    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    error = _validate_business_rules(data)
    if error:
        return jsonify({"message": error}), 400

    try:
        item = space_service.create_space(**data)
        return jsonify(response_schema.dump(item)), 201
    except PermissionError as error:
        return jsonify({"message": str(error)}), 403
    except ValueError as error:
        return jsonify({"message": str(error)}), 400
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to create space"}), 500


@bp.put("/<int:space_id>")
@provider_required
def update_space(space_id):
    if not _owned_space(space_id):
        return jsonify({"message": "Space not found"}), 404

    data = request.get_json(silent=True) or {}
    data.pop("provider_id", None)
    data["provider_id"] = g.provider_id

    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    error = _validate_business_rules(data)
    if error:
        return jsonify({"message": error}), 400

    try:
        item = space_service.update_space(space_id, **data)
        return jsonify(response_schema.dump(item)), 200
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to update space"}), 500


@bp.patch("/<int:space_id>/status")
@provider_required
def update_space_status(space_id):
    if not _owned_space(space_id):
        return jsonify({"message": "Space not found"}), 404

    status = str((request.get_json(silent=True) or {}).get("status", ""))
    status = status.strip().lower()
    if status not in ALLOWED_STATUSES:
        return jsonify({"message": "Invalid space status"}), 400

    try:
        item = space_service.update_space(space_id, status=status)
        return jsonify(response_schema.dump(item)), 200
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to update space status"}), 500


@bp.delete("/<int:space_id>")
@provider_required
def delete_space(space_id):
    if not _owned_space(space_id):
        return jsonify({"message": "Space not found"}), 404

    try:
        space_service.delete_space(space_id)
        return "", 204
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to delete space"}), 500
