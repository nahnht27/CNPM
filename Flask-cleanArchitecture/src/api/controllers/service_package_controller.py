from flask import Blueprint, request, jsonify
from services.service_package_service import ServicePackageService
from infrastructure.repositories.service_package_repository import ServicePackageRepository
from api.schemas.service_package import (
    ServicePackageRequestSchema,
    ServicePackageResponseSchema
)
from infrastructure.databases.mssql import session

bp = Blueprint('service_package', __name__, url_prefix='/service-packages')

service_package_service = ServicePackageService(
    ServicePackageRepository(session)
)

request_schema = ServicePackageRequestSchema()
response_schema = ServicePackageResponseSchema()


@bp.route('/', methods=['GET'])
def list_packages():
    """
    List service packages
    ---
    get:
      summary: Lấy danh sách gói dịch vụ (Có hỗ trợ lọc theo space_id)
      tags:
        - ServicePackage
      parameters:
        - name: space_id
          in: query
          required: false
          schema:
            type: integer
          description: ID của Không gian để lọc các dịch vụ liên quan
      responses:
        200:
          description: Danh sách gói dịch vụ
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ServicePackageResponse'
    """
    # Lấy space_id từ query parameter (ví dụ: /service-packages?space_id=1)
    space_id = request.args.get('space_id', type=int)

    if space_id:
        items = service_package_service.get_packages_by_space(space_id)
    else:
        items = service_package_service.list_packages()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:pkg_id>', methods=['GET'])
def get_package(pkg_id):
    """
    Get service package
    ---
    get:
      summary: Lấy chi tiết gói dịch vụ
      tags:
        - ServicePackage
      parameters:
        - name: pkg_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết gói dịch vụ
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServicePackageResponse'
        404:
          description: Không tìm thấy gói dịch vụ
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = service_package_service.get_package(pkg_id)

    if not item:
        return jsonify({'message': 'Package not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_package():
    """
    Create service package
    ---
    post:
      summary: Tạo gói dịch vụ mới
      tags:
        - ServicePackage
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ServicePackageRequest'
      responses:
        201:
          description: Gói dịch vụ đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServicePackageResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = service_package_service.create_package(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:pkg_id>', methods=['PUT'])
def update_package(pkg_id):
    """
    Update service package
    ---
    put:
      summary: Cập nhật gói dịch vụ
      tags:
        - ServicePackage
      parameters:
        - name: pkg_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ServicePackageRequest'
      responses:
        200:
          description: Gói dịch vụ đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServicePackageResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = service_package_service.update_package(pkg_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:pkg_id>', methods=['DELETE'])
def delete_package(pkg_id):
    """
    Delete service package
    ---
    delete:
      summary: Xóa gói dịch vụ
      tags:
        - ServicePackage
      parameters:
        - name: pkg_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    service_package_service.delete_package(pkg_id)

    return '', 204