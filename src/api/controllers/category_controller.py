from flask import Blueprint, request, jsonify
from services.category_service import CategoryService
from infrastructure.repositories.category_repository import CategoryRepository
from api.schemas.category import CategoryRequestSchema, CategoryResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('category', __name__, url_prefix='/categories')

category_service = CategoryService(CategoryRepository(session))

request_schema = CategoryRequestSchema()
response_schema = CategoryResponseSchema()


@bp.route('/', methods=['GET'])
def list_categories():
    """
    List categories
    ---
    get:
      summary: Lấy danh sách danh mục
      tags:
        - Category
      responses:
        200:
          description: Danh sách danh mục
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CategoryResponse'
    """
    items = category_service.list_categories()
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    """
    Get category
    ---
    get:
      summary: Lấy chi tiết danh mục
      tags:
        - Category
      parameters:
        - name: cat_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết danh mục
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CategoryResponse'
        404:
          description: Không tìm thấy danh mục
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = category_service.get_category(cat_id)

    if not item:
        return jsonify({'message': 'Category not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_category():
    """
    Create category
    ---
    post:
      summary: Tạo danh mục mới
      tags:
        - Category
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CategoryRequest'
      responses:
        201:
          description: Danh mục đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CategoryResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = category_service.create_category(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    """
    Update category
    ---
    put:
      summary: Cập nhật danh mục
      tags:
        - Category
      parameters:
        - name: cat_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CategoryRequest'
      responses:
        200:
          description: Danh mục đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CategoryResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = category_service.update_category(cat_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    """
    Delete category
    ---
    delete:
      summary: Xóa danh mục
      tags:
        - Category
      parameters:
        - name: cat_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    category_service.delete_category(cat_id)

    return '', 204