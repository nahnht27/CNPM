from flask import Blueprint, request, jsonify
from services.ai_configuration_service import AIConfigurationService
from infrastructure.repositories.ai_configuration_repository import AIConfigurationRepository
from api.schemas.ai_configuration import AIConfigurationRequestSchema, AIConfigurationResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('ai_configuration', __name__, url_prefix='/ai-configurations')

ai_configuration_service = AIConfigurationService(AIConfigurationRepository(session))

request_schema = AIConfigurationRequestSchema()
response_schema = AIConfigurationResponseSchema()


@bp.route('/', methods=['GET'])
def list_configs():
    """
    List AI configurations
    ---
    get:
      summary: Lấy danh sách cấu hình AI
      tags:
        - AIConfiguration
      responses:
        200:
          description: Danh sách cấu hình
    """
    items = ai_configuration_service.list_configs()
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:config_id>', methods=['GET'])
def get_config(config_id):
    """
    Get AI configuration
    ---
    get:
      summary: Lấy chi tiết 1 cấu hình AI
      tags:
        - AIConfiguration
      parameters:
        - name: config_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết cấu hình
        404:
          description: Không tìm thấy cấu hình
    """
    item = ai_configuration_service.get_config(config_id)
    if not item:
        return jsonify({'message': 'Config not found'}), 404
    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_config():
    """
    Create AI configuration
    ---
    post:
      summary: Tạo cấu hình AI mới
      tags:
        - AIConfiguration
      responses:
        201:
          description: Cấu hình đã được tạo
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = ai_configuration_service.create_config(**data)
    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:config_id>', methods=['PUT'])
def update_config(config_id):
    """
    Update AI configuration
    ---
    put:
      summary: Cập nhật cấu hình AI
      tags:
        - AIConfiguration
      parameters:
        - name: config_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Cấu hình đã được cập nhật
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = ai_configuration_service.update_config(config_id, **data)
    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:config_id>', methods=['DELETE'])
def delete_config(config_id):
    """
    Delete AI configuration
    ---
    delete:
      summary: Xoá cấu hình AI
      tags:
        - AIConfiguration
      parameters:
        - name: config_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xoá thành công
    """
    ai_configuration_service.delete_config(config_id)
    return '', 204