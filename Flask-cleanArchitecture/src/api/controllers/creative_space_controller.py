from flask import Blueprint, request, jsonify
from services.creative_space_service import CreativeSpaceService
from infrastructure.repositories.creative_space_repository import CreativeSpaceRepository
from api.schemas.creative_space import (
    CreativeSpaceRequestSchema,
    CreativeSpaceResponseSchema
)
from infrastructure.databases.postgres import session

bp = Blueprint('creative_space', __name__, url_prefix='/creative-spaces')

creative_space_service = CreativeSpaceService(
    CreativeSpaceRepository(session)
)

request_schema = CreativeSpaceRequestSchema()
response_schema = CreativeSpaceResponseSchema()


@bp.route('/', methods=['GET'])
def list_spaces():
    """
    List creative spaces
    ---
    get:
      summary: Lấy danh sách không gian sáng tạo
      tags:
        - CreativeSpace
      responses:
        200:
          description: Danh sách không gian sáng tạo
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CreativeSpaceResponse'
    """
    items = creative_space_service.list_spaces()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:space_id>', methods=['GET'])
def get_space(space_id):
    """
    Get creative space
    ---
    get:
      summary: Lấy chi tiết không gian sáng tạo
      tags:
        - CreativeSpace
      parameters:
        - name: space_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết không gian sáng tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreativeSpaceResponse'
        404:
          description: Không tìm thấy không gian sáng tạo
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = creative_space_service.get_space_detail(space_id)

    if not item:
        return jsonify({'message': 'Space not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_space():
    """
    Create creative space
    ---
    post:
      summary: Tạo không gian sáng tạo mới
      tags:
        - CreativeSpace
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreativeSpaceRequest'
      responses:
        201:
          description: Không gian sáng tạo đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreativeSpaceResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = creative_space_service.create_space(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:space_id>', methods=['PUT'])
def update_space(space_id):
    """
    Update creative space
    ---
    put:
      summary: Cập nhật không gian sáng tạo
      tags:
        - CreativeSpace
      parameters:
        - name: space_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreativeSpaceRequest'
      responses:
        200:
          description: Không gian sáng tạo đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreativeSpaceResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = creative_space_service.update_space(space_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:space_id>', methods=['DELETE'])
def delete_space(space_id):
    """
    Delete creative space
    ---
    delete:
      summary: Xóa không gian sáng tạo
      tags:
        - CreativeSpace
      parameters:
        - name: space_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    creative_space_service.delete_space(space_id)

    return '', 204