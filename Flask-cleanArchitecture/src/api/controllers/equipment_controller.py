from flask import Blueprint, request, jsonify
from services.equipment_service import EquipmentService
from infrastructure.repositories.equipment_repository import EquipmentRepository
from api.schemas.equipment import EquipmentRequestSchema, EquipmentResponseSchema
from config import DevelopmentConfig
from infrastructure.databases.postgres import session

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

equipment_service = EquipmentService(
    EquipmentRepository(session)
)

request_schema = EquipmentRequestSchema()
response_schema = EquipmentResponseSchema()
response_list_schema = EquipmentResponseSchema(many=True)


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
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = equipment_service.create_equipment(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:eq_id>', methods=['PUT'])
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
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = equipment_service.update_equipment(eq_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:eq_id>', methods=['DELETE'])
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
    equipment_service.delete_equipment(eq_id)

    return '', 204