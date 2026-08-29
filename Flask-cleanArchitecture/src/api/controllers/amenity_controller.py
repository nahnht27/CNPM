from flask import Blueprint, request, jsonify
from services.amenity_service import AmenityService
from infrastructure.repositories.amenity_repository import AmenityRepository
from api.schemas.amenity import AmenityRequestSchema, AmenityResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('amenity', __name__, url_prefix='/amenities')

amenity_service = AmenityService(AmenityRepository(session))

request_schema = AmenityRequestSchema()
response_schema = AmenityResponseSchema()


@bp.route('/', methods=['GET'])
def list_amenities():
    """
    List amenities
    ---
    get:
      summary: Lấy danh sách tiện ích
      tags:
        - Amenity
      responses:
        200:
          description: Danh sách tiện ích
    """
    items = amenity_service.list_amenities()
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Get amenity
    ---
    get:
      summary: Lấy chi tiết 1 tiện ích
      tags:
        - Amenity
      parameters:
        - name: amenity_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết tiện ích
        404:
          description: Không tìm thấy tiện ích
    """
    item = amenity_service.get_amenity(amenity_id)
    if not item:
        return jsonify({'message': 'Amenity not found'}), 404
    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_amenity():
    """
    Create amenity
    ---
    post:
      summary: Tạo tiện ích mới
      tags:
        - Amenity
      responses:
        201:
          description: Tiện ích đã được tạo
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = amenity_service.create_amenity(**data)
    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Update amenity
    ---
    put:
      summary: Cập nhật tiện ích
      tags:
        - Amenity
      parameters:
        - name: amenity_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Tiện ích đã được cập nhật
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = amenity_service.update_amenity(amenity_id, **data)
    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete amenity
    ---
    delete:
      summary: Xoá tiện ích
      tags:
        - Amenity
      parameters:
        - name: amenity_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xoá thành công
        409:
          description: Không thể xoá vì đang được sử dụng bởi CreativeSpace khác
    """
    amenity_service.delete_amenity(amenity_id)
    return '', 204