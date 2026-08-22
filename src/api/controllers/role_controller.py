from flask import Blueprint, request, jsonify
from services.role_service import RoleService
from infrastructure.repositories.role_repository import RoleRepository
from api.schemas.role import RoleRequestSchema, RoleResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('role', __name__, url_prefix='/roles')

role_service = RoleService(RoleRepository(session))

request_schema = RoleRequestSchema()
response_schema = RoleResponseSchema()


@bp.route('/', methods=['GET'])
def list_roles():
    """
    List roles
    ---
    get:
      summary: Lấy danh sách vai trò
      tags:
        - Role
      responses:
        200:
          description: Danh sách vai trò
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RoleResponse'
    """
    roles = role_service.list_roles()

    return jsonify(response_schema.dump(roles, many=True)), 200


@bp.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """
    Get role
    ---
    get:
      summary: Lấy chi tiết vai trò
      tags:
        - Role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết vai trò
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RoleResponse'
        404:
          description: Không tìm thấy vai trò
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    role = role_service.get_role(role_id)

    if not role:
        return jsonify({'message': 'Role not found'}), 404

    return jsonify(response_schema.dump(role)), 200


@bp.route('/', methods=['POST'])
def create_role():
    """
    Create role
    ---
    post:
      summary: Tạo vai trò mới
      tags:
        - Role
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoleRequest'
      responses:
        201:
          description: Vai trò đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RoleResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    now = datetime.utcnow()

    role = role_service.create_role(
        name=data.get('name'),
        created_at=now,
        created_by=data.get('created_by')
    )

    return jsonify(response_schema.dump(role)), 201


@bp.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    """
    Update role
    ---
    put:
      summary: Cập nhật vai trò
      tags:
        - Role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoleRequest'
      responses:
        200:
          description: Vai trò đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RoleResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    role = role_service.update_role(
        role_id=role_id,
        name=data.get('name'),
        updated_at=datetime.utcnow(),
        updated_by=data.get('updated_by')
    )

    return jsonify(response_schema.dump(role)), 200


@bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """
    Delete role
    ---
    delete:
      summary: Xóa vai trò
      tags:
        - Role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    role_service.delete_role(role_id)

    return '', 204