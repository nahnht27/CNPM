"""Provider-only APIs for managing equipment."""

from datetime import datetime

from flask import Blueprint, g, jsonify, request

from api.provider_space import provider_required
from api.schemas.equipment import EquipmentRequestSchema, EquipmentResponseSchema
from infrastructure.databases.postgres import session
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.equipment_model import EquipmentModel
from infrastructure.repositories.equipment_repository import EquipmentRepository
from services.equipment_service import EquipmentService


bp = Blueprint(
    "provider_equipment",
    __name__,
    url_prefix="/provider/equipment",
)

equipment_service = EquipmentService(EquipmentRepository(session))
request_schema = EquipmentRequestSchema()
response_schema = EquipmentResponseSchema()

ALLOWED_STATUSES = {"available", "unavailable", "maintenance"}


def _owned_equipment(equipment_id):
    return session.query(EquipmentModel).filter(
        EquipmentModel.id == equipment_id,
        EquipmentModel.provider_id == g.provider_id,
    ).first()


def _provider_owns_space(space_id):
    if space_id is None:
        return True

    return session.query(CreativeSpaceModel).filter(
        CreativeSpaceModel.id == space_id,
        CreativeSpaceModel.provider_id == g.provider_id,
    ).first() is not None


def _validate_business_rules(data):
    if data.get("status") not in ALLOWED_STATUSES:
        return "Invalid equipment status"
    if not data.get("condition"):
        return "condition is required"
    if not data.get("purchase_date"):
        return "purchase_date is required"

    try:
        if float(data.get("rental_price")) < 0:
            return "rental_price must not be negative"
    except (TypeError, ValueError):
        return "rental_price must be a valid number"

    if not _provider_owns_space(data.get("space_id")):
        return "Space not found"

    return None


def _normalize_purchase_date(data):
    value = data.get("purchase_date")
    if isinstance(value, str):
        try:
            data["purchase_date"] = datetime.fromisoformat(value)
        except ValueError:
            return "purchase_date must use ISO format"
    return None


@bp.get("")
@bp.get("/")
@provider_required
def list_equipment():
    query = session.query(EquipmentModel).filter(
        EquipmentModel.provider_id == g.provider_id
    )

    space_id = request.args.get("space_id", type=int)
    status = request.args.get("status", type=str)
    if space_id is not None:
        query = query.filter(EquipmentModel.space_id == space_id)
    if status:
        query = query.filter(EquipmentModel.status == status.lower())

    return jsonify(response_schema.dump(query.all(), many=True)), 200


@bp.get("/<int:equipment_id>")
@provider_required
def get_equipment(equipment_id):
    item = _owned_equipment(equipment_id)
    if not item:
        return jsonify({"message": "Equipment not found"}), 404
    return jsonify(response_schema.dump(item)), 200


@bp.post("")
@bp.post("/")
@provider_required
def create_equipment():
    data = request.get_json(silent=True) or {}
    data.pop("provider_id", None)
    data["provider_id"] = g.provider_id

    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    error = _validate_business_rules(data) or _normalize_purchase_date(data)
    if error:
        return jsonify({"message": error}), 400

    try:
        item = equipment_service.create_equipment(**data)
        return jsonify(response_schema.dump(item)), 201
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to create equipment"}), 500


@bp.put("/<int:equipment_id>")
@provider_required
def update_equipment(equipment_id):
    if not _owned_equipment(equipment_id):
        return jsonify({"message": "Equipment not found"}), 404

    data = request.get_json(silent=True) or {}
    data.pop("provider_id", None)
    data["provider_id"] = g.provider_id

    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    error = _validate_business_rules(data) or _normalize_purchase_date(data)
    if error:
        return jsonify({"message": error}), 400

    try:
        item = equipment_service.update_equipment(equipment_id, **data)
        return jsonify(response_schema.dump(item)), 200
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to update equipment"}), 500


@bp.patch("/<int:equipment_id>/status")
@provider_required
def update_equipment_status(equipment_id):
    if not _owned_equipment(equipment_id):
        return jsonify({"message": "Equipment not found"}), 404

    status = str((request.get_json(silent=True) or {}).get("status", ""))
    status = status.strip().lower()
    if status not in ALLOWED_STATUSES:
        return jsonify({"message": "Invalid equipment status"}), 400

    try:
        item = equipment_service.update_equipment(equipment_id, status=status)
        return jsonify(response_schema.dump(item)), 200
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to update equipment status"}), 500


@bp.delete("/<int:equipment_id>")
@provider_required
def delete_equipment(equipment_id):
    if not _owned_equipment(equipment_id):
        return jsonify({"message": "Equipment not found"}), 404

    try:
        equipment_service.delete_equipment(equipment_id)
        return "", 204
    except Exception:
        session.rollback()
        return jsonify({"message": "Unable to delete equipment"}), 500
