from functools import wraps

import jwt
from flask import Blueprint, current_app, g, jsonify, request
from services.equipment_service import EquipmentService
from infrastructure.repositories.equipment_repository import EquipmentRepository
from api.schemas.equipment import EquipmentRequestSchema, EquipmentResponseSchema
from config import DevelopmentConfig
from infrastructure.databases.postgres import session
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.equipment_model import EquipmentModel

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

equipment_service = EquipmentService(
    EquipmentRepository(session)
)

request_schema = EquipmentRequestSchema()
response_schema = EquipmentResponseSchema()
response_list_schema = EquipmentResponseSchema(many=True)

EQUIPMENT_STATUSES = {'available', 'unavailable', 'maintenance'}


def provider_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get('Authorization', '')
        if not authorization.startswith('Bearer '):
            return jsonify({'message': 'Authentication is required'}), 401

        try:
            payload = jwt.decode(
                authorization[7:].strip(),
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        try:
            role_id = int(payload.get('role_id'))
            provider_id = int(payload.get('provider_id'))
        except (TypeError, ValueError):
            return jsonify({'message': 'Provider access is required'}), 403

        if role_id != 3:
            return jsonify({'message': 'Provider access is required'}), 403

        g.provider_id = provider_id
        return view(*args, **kwargs)

    return wrapped


def get_owned_equipment(equipment_id):
    return session.query(EquipmentModel).filter(
        EquipmentModel.id == equipment_id,
        EquipmentModel.provider_id == g.provider_id
    ).first()


def provider_owns_space(space_id):
    if space_id is None:
        return True

    return session.query(CreativeSpaceModel).filter(
        CreativeSpaceModel.id == space_id,
        CreativeSpaceModel.provider_id == g.provider_id
    ).first() is not None


def validate_equipment_data(data):
    if data.get('status') not in EQUIPMENT_STATUSES:
        return 'Invalid equipment status'

    if not data.get('condition'):
        return 'condition is required'

    if not data.get('purchase_date'):
        return 'purchase_date is required'

    try:
        if float(data.get('rental_price')) < 0:
            return 'rental_price must not be negative'
    except (TypeError, ValueError):
        return 'rental_price must be a valid number'

    if not provider_owns_space(data.get('space_id')):
        return 'Space not found'

    return None


@bp.route('/', methods=['GET'])
def list_equipment():
    """
    List equipment
    ---
    get:
      summary: Lấy danh sách thiết bị (Có hỗ trợ lọc theo space_id)
      tags:
        - Equipment
      parameters:
        - name: space_id
          in: query
          required: false
          schema:
            type: integer
          description: Lọc thiết bị theo ID không gian
      responses:
        200:
          description: Danh sách thiết bị
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/EquipmentResponse'
    """
    space_id = request.args.get('space_id', type=int)
    items = equipment_service.list_equipment(space_id=space_id)
    return jsonify(response_list_schema.dump(items)), 200


@bp.route('/mine', methods=['GET'])
@provider_required
def list_my_equipment():
    space_id = request.args.get('space_id', type=int)
    query = session.query(EquipmentModel).filter(
        EquipmentModel.provider_id == g.provider_id
    )

    if space_id is not None:
        query = query.filter(EquipmentModel.space_id == space_id)

    items = query.all()
    return jsonify(response_list_schema.dump(items)), 200

@bp.route('/<int:eq_id>', methods=['GET'])
def get_equipment(eq_id):
    """
    Get equipment
    ---
    get:
      summary: Lấy chi tiết thiết bị
      tags:
        - Equipment
      parameters:
        - name: eq_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết thiết bị
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EquipmentResponse'
        404:
          description: Không tìm thấy thiết bị
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = equipment_service.get_equipment(eq_id)

    if not item:
        return jsonify({'message': 'Equipment not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
@provider_required
def create_equipment():
    """
    Create equipment
    ---
    post:
      summary: Tạo thiết bị mới
      tags:
        - Equipment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EquipmentRequest'
      responses:
        201:
          description: Thiết bị đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EquipmentResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json(silent=True) or {}
    data.pop('provider_id', None)
    data['provider_id'] = g.provider_id

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    validation_error = validate_equipment_data(data)
    if validation_error:
        return jsonify({'message': validation_error}), 400

    try:
        item = equipment_service.create_equipment(**data)
    except Exception:
        session.rollback()
        raise

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:eq_id>', methods=['PUT'])
@provider_required
def update_equipment(eq_id):
    """
    Update equipment
    ---
    put:
      summary: Cập nhật thiết bị
      tags:
        - Equipment
      parameters:
        - name: eq_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EquipmentRequest'
      responses:
        200:
          description: Thiết bị đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EquipmentResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    if not get_owned_equipment(eq_id):
        return jsonify({'message': 'Equipment not found'}), 404

    data = request.get_json(silent=True) or {}
    data.pop('provider_id', None)
    data['provider_id'] = g.provider_id

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    validation_error = validate_equipment_data(data)
    if validation_error:
        return jsonify({'message': validation_error}), 400

    try:
        item = equipment_service.update_equipment(eq_id, **data)
    except Exception:
        session.rollback()
        raise

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:eq_id>/status', methods=['PATCH'])
@provider_required
def update_equipment_status(eq_id):
    if not get_owned_equipment(eq_id):
        return jsonify({'message': 'Equipment not found'}), 404

    data = request.get_json(silent=True) or {}
    status = str(data.get('status', '')).strip().lower()
    if status not in EQUIPMENT_STATUSES:
        return jsonify({'message': 'Invalid equipment status'}), 400

    try:
        item = equipment_service.update_equipment(eq_id, status=status)
    except Exception:
        session.rollback()
        raise

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:eq_id>', methods=['DELETE'])
@provider_required
def delete_equipment(eq_id):
    """
    Delete equipment
    ---
    delete:
      summary: Xóa thiết bị
      tags:
        - Equipment
      parameters:
        - name: eq_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    if not get_owned_equipment(eq_id):
        return jsonify({'message': 'Equipment not found'}), 404

    try:
        equipment_service.delete_equipment(eq_id)
    except Exception:
        session.rollback()
        raise

    return '', 204
