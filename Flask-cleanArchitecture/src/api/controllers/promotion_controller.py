from flask import Blueprint, request, jsonify
from services.promotion_service import PromotionService
from infrastructure.repositories.promotion_repository import PromotionRepository
from api.schemas.promotion import PromotionRequestSchema, PromotionResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('promotion', __name__, url_prefix='/promotions')

promotion_service = PromotionService(PromotionRepository(session))

request_schema = PromotionRequestSchema()
response_schema = PromotionResponseSchema()


@bp.route('/', methods=['GET'])
def list_promotions():
    """
    List promotions
    ---
    get:
      summary: Lấy danh sách khuyến mãi
      tags:
        - Promotion
      responses:
        200:
          description: Danh sách khuyến mãi
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PromotionResponse'
    """
    items = promotion_service.list_promotions()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:prom_id>', methods=['GET'])
def get_promotion(prom_id):
    """
    Get promotion
    ---
    get:
      summary: Lấy chi tiết khuyến mãi
      tags:
        - Promotion
      parameters:
        - name: prom_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết khuyến mãi
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PromotionResponse'
        404:
          description: Không tìm thấy khuyến mãi
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = promotion_service.get_promotion(prom_id)

    if not item:
        return jsonify({'message': 'Promotion not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_promotion():
    """
    Create promotion
    ---
    post:
      summary: Tạo khuyến mãi mới
      tags:
        - Promotion
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PromotionRequest'
      responses:
        201:
          description: Khuyến mãi đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PromotionResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = promotion_service.create_promotion(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:prom_id>', methods=['PUT'])
def update_promotion(prom_id):
    """
    Update promotion
    ---
    put:
      summary: Cập nhật khuyến mãi
      tags:
        - Promotion
      parameters:
        - name: prom_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PromotionRequest'
      responses:
        200:
          description: Khuyến mãi đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PromotionResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = promotion_service.update_promotion(prom_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:prom_id>', methods=['DELETE'])
def delete_promotion(prom_id):
    """
    Delete promotion
    ---
    delete:
      summary: Xóa khuyến mãi
      tags:
        - Promotion
      parameters:
        - name: prom_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    promotion_service.delete_promotion(prom_id)

    return '', 204