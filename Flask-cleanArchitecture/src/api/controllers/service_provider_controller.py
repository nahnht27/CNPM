from flask import Blueprint, request, jsonify
from services.service_provider_service import ServiceProviderService
from infrastructure.repositories.service_provider_repository import (
    ServiceProviderRepository
)
from api.schemas.service_provider import (
    ServiceProviderRequestSchema,
    ServiceProviderResponseSchema
)
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint(
    'service_provider',
    __name__,
    url_prefix='/service-providers'
)

service_provider_service = ServiceProviderService(
    ServiceProviderRepository(session)
)

request_schema = ServiceProviderRequestSchema()
response_schema = ServiceProviderResponseSchema()


@bp.route('/', methods=['GET'])
def list_providers():
    """
    List service providers
    ---
    get:
      summary: Lấy danh sách nhà cung cấp dịch vụ
      tags:
        - ServiceProvider
      responses:
        200:
          description: Danh sách nhà cung cấp dịch vụ
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ServiceProviderResponse'
    """
    providers = service_provider_service.list_providers()

    return jsonify(response_schema.dump(providers, many=True)), 200


@bp.route('/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    """
    Get service provider
    ---
    get:
      summary: Lấy chi tiết nhà cung cấp dịch vụ
      tags:
        - ServiceProvider
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết nhà cung cấp dịch vụ
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServiceProviderResponse'
        404:
          description: Không tìm thấy nhà cung cấp dịch vụ
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    prov = service_provider_service.get_provider(provider_id)

    if not prov:
        return jsonify({'message': 'Provider not found'}), 404

    return jsonify(response_schema.dump(prov)), 200


@bp.route('/', methods=['POST'])
def create_provider():
    """
    Create service provider
    ---
    post:
      summary: Tạo nhà cung cấp dịch vụ mới
      tags:
        - ServiceProvider
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ServiceProviderRequest'
      responses:
        201:
          description: Nhà cung cấp dịch vụ đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServiceProviderResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    prov = service_provider_service.create_provider(**data)

    return jsonify(response_schema.dump(prov)), 201


@bp.route('/<int:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    """
    Update service provider
    ---
    put:
      summary: Cập nhật nhà cung cấp dịch vụ
      tags:
        - ServiceProvider
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ServiceProviderRequest'
      responses:
        200:
          description: Nhà cung cấp dịch vụ đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ServiceProviderResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    prov = service_provider_service.update_provider(
        provider_id,
        **data
    )

    return jsonify(response_schema.dump(prov)), 200


@bp.route('/<int:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):
    """
    Delete service provider
    ---
    delete:
      summary: Xóa nhà cung cấp dịch vụ
      tags:
        - ServiceProvider
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    service_provider_service.delete_provider(provider_id)

    return '', 204