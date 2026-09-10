"""Provider-only APIs for managing service packages."""

from flask import Blueprint, g, jsonify, request

from api.provider_space import provider_required
from api.schemas.service_package import (
    ServicePackageRequestSchema,
    ServicePackageResponseSchema,
)
from infrastructure.databases.postgres import session
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.package_detail_model import PackageDetailModel
from infrastructure.models.service_package_model import ServicePackageModel
from infrastructure.repositories.service_package_repository import (
    ServicePackageRepository,
)
from services.service_package_service import ServicePackageService


bp = Blueprint(
    "provider_package",
    __name__,
    url_prefix="/provider/packages",
)

package_service = ServicePackageService(ServicePackageRepository(session))
request_schema = ServicePackageRequestSchema()
response_schema = ServicePackageResponseSchema()

ALLOWED_STATUSES = {"active", "inactive"}


def _owned_package(package_id):
    return session.query(ServicePackageModel).filter(
        ServicePackageModel.id == package_id,
        ServicePackageModel.provider_id == g.provider_id,
    ).first()


def _provider_owns_space(space_id):
    if space_id is None:
        return True

    return session.query(CreativeSpaceModel).filter(
        CreativeSpaceModel.id == space_id,
        CreativeSpaceModel.provider_id == g.provider_id,
    ).first() is not None


def _attach_space_id(items):
    for item in items:
        detail = session.query(PackageDetailModel).filter(
            PackageDetailModel.package_id == item.id,
            PackageDetailModel.item_type == "space",
        ).first()
        item.space_id = detail.reference_id if detail else None
    return items


def _validate_business_rules(data):
    if data.get("status") not in ALLOWED_STATUSES:
        return "Status must be active or inactive"
    try:
        if float(data.get("price")) <= 0:
            return "price must be greater than 0"
    except (TypeError, ValueError):
        return "price must be a valid number"
    if not _provider_owns_space(data.get("space_id")):
        return "Space not found"
    return None


@bp.get("")
@bp.get("/")
@provider_required
def list_packages():
    query = session.query(ServicePackageModel).filter(
        ServicePackageModel.provider_id == g.provider_id
    )

    space_id = request.args.get("space_id", type=int)
    if space_id is not None:
        if not _provider_owns_space(space_id):
            return jsonify({"message": "Space not found"}), 404
        query = query.join(
            PackageDetailModel,
            ServicePackageModel.id == PackageDetailModel.package_id,
        ).filter(
            PackageDetailModel.item_type == "space",
            PackageDetailModel.reference_id == space_id,
        )

    items = _attach_space_id(query.all())
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.get("/<int:package_id>")
@provider_required
def get_package(package_id):
    item = _owned_package(package_id)
    if not item:
        return jsonify({"message": "Package not found"}), 404
    _attach_space_id([item])
    return jsonify(response_schema.dump(item)), 200


@bp.post("")
@bp.post("/")
@provider_required
def create_package():
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
        item = package_service.create_package(**data)
        return jsonify(response_schema.dump(item)), 201
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to create package"}), 500


@bp.put("/<int:package_id>")
@provider_required
def update_package(package_id):
    if not _owned_package(package_id):
        return jsonify({"message": "Package not found"}), 404

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
        item = package_service.update_package(package_id, **data)
        return jsonify(response_schema.dump(item)), 200
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to update package"}), 500


@bp.patch("/<int:package_id>/status")
@provider_required
def update_package_status(package_id):
    if not _owned_package(package_id):
        return jsonify({"message": "Package not found"}), 404

    status = str((request.get_json(silent=True) or {}).get("status", ""))
    status = status.strip().lower()
    if status not in ALLOWED_STATUSES:
        return jsonify({"message": "Invalid package status"}), 400

    try:
        item = package_service.update_package(package_id, status=status)
        return jsonify(response_schema.dump(item)), 200
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to update package status"}), 500


@bp.delete("/<int:package_id>")
@provider_required
def delete_package(package_id):
    if not _owned_package(package_id):
        return jsonify({"message": "Package not found"}), 404

    try:
        package_service.delete_package(package_id)
        return "", 204
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to delete package"}), 500
