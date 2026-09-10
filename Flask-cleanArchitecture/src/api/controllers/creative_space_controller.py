from functools import wraps

import jwt
from flask import Blueprint, current_app, g, jsonify, request

from services.creative_space_service import (
    CreativeSpaceService
)

from infrastructure.repositories.creative_space_repository import (
    CreativeSpaceRepository
)

from infrastructure.repositories.service_provider_repository import (
    ServiceProviderRepository
)

from api.schemas.creative_space import (
    CreativeSpaceRequestSchema,
    CreativeSpaceResponseSchema
)

from infrastructure.databases.postgres import session
from infrastructure.models.creative_space_model import CreativeSpaceModel


bp = Blueprint(
    'creative_space',
    __name__,
    url_prefix='/creative-spaces'
)


# =========================================================
# REPOSITORIES + SERVICE
# =========================================================

creative_space_service = CreativeSpaceService(
    CreativeSpaceRepository(session),
    ServiceProviderRepository(session)
)


request_schema = CreativeSpaceRequestSchema()
response_schema = CreativeSpaceResponseSchema()

SPACE_STATUSES = {'active', 'inactive'}


def provider_required(view):
    """Authenticate a Service Provider and expose its id through ``g``."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get('Authorization', '')

        if not authorization.startswith('Bearer '):
            return jsonify({'message': 'Authentication is required'}), 401

        token = authorization[7:].strip()

        try:
            payload = jwt.decode(
                token,
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


def get_owned_space(space_id):
    return session.query(CreativeSpaceModel).filter(
        CreativeSpaceModel.id == space_id,
        CreativeSpaceModel.provider_id == g.provider_id
    ).first()


def validate_space_data(data):
    if data.get('status') not in SPACE_STATUSES:
        return 'Status must be active or inactive'

    positive_fields = ('max_capacity', 'base_price')

    for field in positive_fields:
        try:
            if float(data.get(field)) <= 0:
                return f'{field} must be greater than 0'
        except (TypeError, ValueError):
            return f'{field} must be a valid number'

    size_sqm = data.get('size_sqm')
    if size_sqm is not None:
        try:
            if float(size_sqm) <= 0:
                return 'size_sqm must be greater than 0'
        except (TypeError, ValueError):
            return 'size_sqm must be a valid number'

    return None


# =========================================================
# GET ALL
# =========================================================

@bp.route('/', methods=['GET'])
def list_spaces():
    """
    List creative spaces
    ---
    get:
      summary: Lấy danh sách không gian sáng tạo
      tags:
        - CreativeSpace
      parameters:
        - name: provider_id
          in: query
          required: false
          schema:
            type: integer
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

    provider_id = request.args.get(
        'provider_id',
        type=int
    )

    items = creative_space_service.list_spaces(
        provider_id=provider_id
    )

    return jsonify(
        response_schema.dump(
            items,
            many=True
        )
    ), 200


# =========================================================
# GET CURRENT PROVIDER'S SPACES
# =========================================================

@bp.route('/mine', methods=['GET'])
@provider_required
def list_my_spaces():
    items = creative_space_service.list_spaces(
        provider_id=g.provider_id
    )

    return jsonify(
        response_schema.dump(items, many=True)
    ), 200


# =========================================================
# GET DETAIL
# =========================================================

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
    """

    item = creative_space_service.get_space_detail(
        space_id
    )

    if not item:
        return jsonify({
            'message': 'Space not found'
        }), 404

    return jsonify(
        response_schema.dump(item)
    ), 200


# =========================================================
# CREATE
# =========================================================

@bp.route('/', methods=['POST'])
@provider_required
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
        403:
          description: Provider chưa được Admin xác minh
    """

    data = request.get_json(silent=True) or {}

    # -----------------------------------------------------
    # Kiểm tra body
    # -----------------------------------------------------

    if not data:
        return jsonify({
            'message': 'Request body is required'
        }), 400

    # -----------------------------------------------------
    # Validate dữ liệu
    # -----------------------------------------------------

    data.pop('provider_id', None)
    data['provider_id'] = g.provider_id

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    validation_error = validate_space_data(data)
    if validation_error:
        return jsonify({'message': validation_error}), 400

    # -----------------------------------------------------
    # Kiểm tra Provider verification
    # -----------------------------------------------------

    try:

        item = creative_space_service.create_space(
            **data
        )

        return jsonify(
            response_schema.dump(item)
        ), 201

    except PermissionError as e:

        return jsonify({
            'message': str(e)
        }), 403

    except ValueError as e:

        return jsonify({
            'message': str(e)
        }), 400


# =========================================================
# UPDATE
# =========================================================

@bp.route('/<int:space_id>', methods=['PUT'])
@provider_required
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

    if not get_owned_space(space_id):
        return jsonify({'message': 'Space not found'}), 404

    data = request.get_json(silent=True) or {}

    if not data:
        return jsonify({
            'message': 'Request body is required'
        }), 400

    data.pop('provider_id', None)
    data['provider_id'] = g.provider_id

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    validation_error = validate_space_data(data)
    if validation_error:
        return jsonify({'message': validation_error}), 400

    try:

        item = creative_space_service.update_space(
            space_id,
            **data
        )

        return jsonify(
            response_schema.dump(item)
        ), 200

    except ValueError as e:

        return jsonify({
            'message': str(e)
        }), 404


# =========================================================
# UPDATE STATUS
# =========================================================

@bp.route('/<int:space_id>/status', methods=['PATCH'])
@provider_required
def update_space_status(space_id):
    if not get_owned_space(space_id):
        return jsonify({'message': 'Space not found'}), 404

    data = request.get_json(silent=True) or {}
    status = str(data.get('status', '')).strip().lower()

    if status not in SPACE_STATUSES:
        return jsonify({
            'message': 'Status must be active or inactive'
        }), 400

    item = creative_space_service.update_space(
        space_id,
        status=status
    )

    return jsonify(response_schema.dump(item)), 200


# =========================================================
# DELETE
# =========================================================

@bp.route('/<int:space_id>', methods=['DELETE'])
@provider_required
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

    if not get_owned_space(space_id):
        return jsonify({'message': 'Space not found'}), 404

    creative_space_service.delete_space(
        space_id
    )

    return '', 204
