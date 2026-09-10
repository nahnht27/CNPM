from functools import wraps

import jwt
from flask import Blueprint, current_app, g, jsonify, request
from services.service_package_service import ServicePackageService
from infrastructure.repositories.service_package_repository import ServicePackageRepository
from api.schemas.service_package import (
    ServicePackageRequestSchema,
    ServicePackageResponseSchema
)
from infrastructure.databases.postgres import session
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.package_detail_model import PackageDetailModel
from infrastructure.models.service_package_model import ServicePackageModel

bp = Blueprint('service_package', __name__, url_prefix='/service-packages')

service_package_service = ServicePackageService(
    ServicePackageRepository(session)
)

request_schema = ServicePackageRequestSchema()
response_schema = ServicePackageResponseSchema()
response_list_schema = ServicePackageResponseSchema(many=True)

PACKAGE_STATUSES = {'active', 'inactive'}


def provider_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get('Authorization', '')
        if not authorization.startswith('Bearer '):
            return jsonify({'message': 'Authentication is required'}), 401

        try:
            payload = jwt.decode(
                authorization[7:].strip(),
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        try:
            role_id = int(payload.get('role_id'))
            provider_id = int(payload.get('provider_id'))
        except (TypeError, ValueError):
            return jsonify({'message': 'Provider access is required'}), 403

        if role_id != 3:
            return jsonify({'message': 'Provider access is required'}), 403

        g.provider_id = provider_id
        return view(*args, **kwargs)

    return wrapped


def get_owned_package(package_id):
    return session.query(ServicePackageModel).filter(
        ServicePackageModel.id == package_id,
        ServicePackageModel.provider_id == g.provider_id
    ).first()


def provider_owns_space(space_id):
    if space_id is None:
        return True

    return session.query(CreativeSpaceModel).filter(
        CreativeSpaceModel.id == space_id,
        CreativeSpaceModel.provider_id == g.provider_id
    ).first() is not None


def validate_package_data(data):
    if data.get('status') not in PACKAGE_STATUSES:
        return 'Status must be active or inactive'

    try:
        if float(data.get('price')) <= 0:
            return 'price must be greater than 0'
    except (TypeError, ValueError):
        return 'price must be a valid number'

    if not provider_owns_space(data.get('space_id')):
        return 'Space not found'

    return None


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

    # Dùng response_list_schema thay vì response_schema.dump(..., many=True)
    return jsonify(response_list_schema.dump(items)), 200


@bp.route('/mine', methods=['GET'])
@provider_required
def list_my_packages():
    space_id = request.args.get('space_id', type=int)

    if space_id is not None and not provider_owns_space(space_id):
        return jsonify({'message': 'Space not found'}), 404

    query = session.query(ServicePackageModel).filter(
        ServicePackageModel.provider_id == g.provider_id
    )

    if space_id is not None:
        query = query.join(
            PackageDetailModel,
            ServicePackageModel.id == PackageDetailModel.package_id
        ).filter(
            PackageDetailModel.item_type == 'space',
            PackageDetailModel.reference_id == space_id
        )

    items = query.all()

    for item in items:
        detail = session.query(PackageDetailModel).filter(
            PackageDetailModel.package_id == item.id,
            PackageDetailModel.item_type == 'space'
        ).first()
        item.space_id = detail.reference_id if detail else None

    return jsonify(response_list_schema.dump(items)), 200


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
@provider_required
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
    data = request.get_json(silent=True) or {}
    data.pop('provider_id', None)
    data['provider_id'] = g.provider_id

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    validation_error = validate_package_data(data)
    if validation_error:
        return jsonify({'message': validation_error}), 400

    try:
        item = service_package_service.create_package(**data)
    except Exception:
        session.rollback()
        raise

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:pkg_id>', methods=['PUT'])
@provider_required
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
    if not get_owned_package(pkg_id):
        return jsonify({'message': 'Package not found'}), 404

    data = request.get_json(silent=True) or {}
    data.pop('provider_id', None)
    data['provider_id'] = g.provider_id

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    validation_error = validate_package_data(data)
    if validation_error:
        return jsonify({'message': validation_error}), 400

    try:
        item = service_package_service.update_package(pkg_id, **data)
    except Exception:
        session.rollback()
        raise

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:pkg_id>/status', methods=['PATCH'])
@provider_required
def update_package_status(pkg_id):
    if not get_owned_package(pkg_id):
        return jsonify({'message': 'Package not found'}), 404

    data = request.get_json(silent=True) or {}
    status = str(data.get('status', '')).strip().lower()
    if status not in PACKAGE_STATUSES:
        return jsonify({
            'message': 'Status must be active or inactive'
        }), 400

    try:
        item = service_package_service.update_package(pkg_id, status=status)
    except Exception:
        session.rollback()
        raise

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:pkg_id>', methods=['DELETE'])
@provider_required
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
    if not get_owned_package(pkg_id):
        return jsonify({'message': 'Package not found'}), 404

    try:
        service_package_service.delete_package(pkg_id)
    except Exception:
        session.rollback()
        raise

    return '', 204
