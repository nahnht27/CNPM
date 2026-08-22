from flask import Blueprint, request, jsonify
from services.review_service import ReviewService
from infrastructure.repositories.review_repository import ReviewRepository
from api.schemas.review import ReviewRequestSchema, ReviewResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('review', __name__, url_prefix='/reviews')

review_service = ReviewService(ReviewRepository(session))

request_schema = ReviewRequestSchema()
response_schema = ReviewResponseSchema()


@bp.route('/', methods=['GET'])
def list_reviews():
    """
    List reviews
    ---
    get:
      summary: Lấy danh sách đánh giá
      tags:
        - Review
      responses:
        200:
          description: Danh sách đánh giá
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewResponse'
    """
    items = review_service.list_reviews()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:rid>', methods=['GET'])
def get_review(rid):
    """
    Get review
    ---
    get:
      summary: Lấy chi tiết đánh giá
      tags:
        - Review
      parameters:
        - name: rid
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết đánh giá
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        404:
          description: Không tìm thấy đánh giá
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = review_service.get_review(rid)

    if not item:
        return jsonify({'message': 'Review not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_review():
    """
    Create review
    ---
    post:
      summary: Tạo đánh giá mới
      tags:
        - Review
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewRequest'
      responses:
        201:
          description: Đánh giá đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = review_service.create_review(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:rid>', methods=['PUT'])
def update_review(rid):
    """
    Update review
    ---
    put:
      summary: Cập nhật đánh giá
      tags:
        - Review
      parameters:
        - name: rid
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewRequest'
      responses:
        200:
          description: Đánh giá đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = review_service.update_review(rid, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:rid>', methods=['DELETE'])
def delete_review(rid):
    """
    Delete review
    ---
    delete:
      summary: Xóa đánh giá
      tags:
        - Review
      parameters:
        - name: rid
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    review_service.delete_review(rid)

    return '', 204