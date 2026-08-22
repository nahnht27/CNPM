from flask import Blueprint, request, jsonify
from services.workshop_service import WorkshopService
from infrastructure.repositories.workshop_repository import WorkshopRepository
from api.schemas.workshop import WorkshopRequestSchema, WorkshopResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('workshop', __name__, url_prefix='/workshops')

workshop_service = WorkshopService(WorkshopRepository(session))

request_schema = WorkshopRequestSchema()
response_schema = WorkshopResponseSchema()


@bp.route('/', methods=['GET'])
def list_workshops():
    """
    List workshops
    ---
    get:
      summary: Lấy danh sách workshop
      tags:
        - Workshop
      responses:
        200:
          description: Danh sách workshop
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkshopResponse'
    """
    items = workshop_service.list_workshops()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:ws_id>', methods=['GET'])
def get_workshop(ws_id):
    """
    Get workshop
    ---
    get:
      summary: Lấy chi tiết workshop
      tags:
        - Workshop
      parameters:
        - name: ws_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết workshop
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkshopResponse'
        404:
          description: Không tìm thấy workshop
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = workshop_service.get_workshop(ws_id)

    if not item:
        return jsonify({'message': 'Workshop not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_workshop():
    """
    Create workshop
    ---
    post:
      summary: Tạo workshop mới
      tags:
        - Workshop
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkshopRequest'
      responses:
        201:
          description: Workshop đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkshopResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = workshop_service.create_workshop(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:ws_id>', methods=['PUT'])
def update_workshop(ws_id):
    """
    Update workshop
    ---
    put:
      summary: Cập nhật workshop
      tags:
        - Workshop
      parameters:
        - name: ws_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkshopRequest'
      responses:
        200:
          description: Workshop đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkshopResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = workshop_service.update_workshop(ws_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:ws_id>', methods=['DELETE'])
def delete_workshop(ws_id):
    """
    Delete workshop
    ---
    delete:
      summary: Xóa workshop
      tags:
        - Workshop
      parameters:
        - name: ws_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    workshop_service.delete_workshop(ws_id)

    return '', 204