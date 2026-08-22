from flask import Blueprint, request, jsonify
from services.consumable_service import ConsumableService
from infrastructure.repositories.consumable_repository import ConsumableRepository
from api.schemas.consumable import ConsumableRequestSchema, ConsumableResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('consumable', __name__, url_prefix='/consumables')

consumable_service = ConsumableService(ConsumableRepository(session))

request_schema = ConsumableRequestSchema()
response_schema = ConsumableResponseSchema()


@bp.route('/', methods=['GET'])
def list_consumables():
    """
    List consumables
    ---
    get:
      summary: Lấy danh sách vật tư tiêu hao
      tags:
        - Consumable
      responses:
        200:
          description: Danh sách vật tư tiêu hao
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ConsumableResponse'
    """
    items = consumable_service.list_consumables()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:consumable_id>', methods=['GET'])
def get_consumable(consumable_id):
    """
    Get consumable
    ---
    get:
      summary: Lấy chi tiết vật tư tiêu hao
      tags:
        - Consumable
      parameters:
        - name: consumable_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết vật tư tiêu hao
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConsumableResponse'
        404:
          description: Không tìm thấy vật tư tiêu hao
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = consumable_service.get_consumable(consumable_id)

    if not item:
        return jsonify({'message': 'Consumable not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_consumable():
    """
    Create consumable
    ---
    post:
      summary: Tạo vật tư tiêu hao mới
      tags:
        - Consumable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConsumableRequest'
      responses:
        201:
          description: Vật tư tiêu hao đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConsumableResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = consumable_service.create_consumable(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:consumable_id>', methods=['PUT'])
def update_consumable(consumable_id):
    """
    Update consumable
    ---
    put:
      summary: Cập nhật vật tư tiêu hao
      tags:
        - Consumable
      parameters:
        - name: consumable_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConsumableRequest'
      responses:
        200:
          description: Vật tư tiêu hao đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConsumableResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = consumable_service.update_consumable(
        consumable_id,
        **data
    )

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:consumable_id>', methods=['DELETE'])
def delete_consumable(consumable_id):
    """
    Delete consumable
    ---
    delete:
      summary: Xóa vật tư tiêu hao
      tags:
        - Consumable
      parameters:
        - name: consumable_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    consumable_service.delete_consumable(consumable_id)

    return '', 204