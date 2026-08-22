from flask import Blueprint, request, jsonify
from services.post_service import PostService
from infrastructure.repositories.post_repository import PostRepository
from api.schemas.post import PostRequestSchema, PostResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('post', __name__, url_prefix='/posts')

post_service = PostService(PostRepository(session))

request_schema = PostRequestSchema()
response_schema = PostResponseSchema()


@bp.route('/', methods=['GET'])
def list_posts():
    """
    List posts
    ---
    get:
      summary: Lấy danh sách bài viết
      tags:
        - Post
      responses:
        200:
          description: Danh sách bài viết
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PostResponse'
    """
    items = post_service.list_posts()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get post
    ---
    get:
      summary: Lấy chi tiết bài viết
      tags:
        - Post
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết bài viết
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostResponse'
        404:
          description: Không tìm thấy bài viết
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = post_service.get_post(post_id)

    if not item:
        return jsonify({'message': 'Post not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_post():
    """
    Create post
    ---
    post:
      summary: Tạo bài viết mới
      tags:
        - Post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostRequest'
      responses:
        201:
          description: Bài viết đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = post_service.create_post(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update post
    ---
    put:
      summary: Cập nhật bài viết
      tags:
        - Post
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostRequest'
      responses:
        200:
          description: Bài viết đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = post_service.update_post(post_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete post
    ---
    delete:
      summary: Xóa bài viết
      tags:
        - Post
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    post_service.delete_post(post_id)

    return '', 204