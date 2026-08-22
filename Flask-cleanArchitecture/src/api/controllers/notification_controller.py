from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService
from infrastructure.repositories.notification_repository import NotificationRepository
from api.schemas.notification import (
    NotificationRequestSchema,
    NotificationResponseSchema
)
from infrastructure.databases.mssql import session

bp = Blueprint('notification', __name__, url_prefix='/notifications')

notification_service = NotificationService(
    NotificationRepository(session)
)

request_schema = NotificationRequestSchema()
response_schema = NotificationResponseSchema()


@bp.route('/', methods=['GET'])
def list_notifications():
    """
    List notifications
    ---
    get:
      summary: Lấy danh sách thông báo
      tags:
        - Notification
      responses:
        200:
          description: Danh sách thông báo
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/NotificationResponse'
    """
    items = notification_service.list_notifications()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:not_id>', methods=['GET'])
def get_notification(not_id):
    """
    Get notification
    ---
    get:
      summary: Lấy chi tiết thông báo
      tags:
        - Notification
      parameters:
        - name: not_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết thông báo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NotificationResponse'
        404:
          description: Không tìm thấy thông báo
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = notification_service.get_notification(not_id)

    if not item:
        return jsonify({'message': 'Notification not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_notification():
    """
    Create notification
    ---
    post:
      summary: Tạo thông báo mới
      tags:
        - Notification
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NotificationRequest'
      responses:
        201:
          description: Thông báo đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NotificationResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = notification_service.create_notification(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:not_id>', methods=['PUT'])
def update_notification(not_id):
    """
    Update notification
    ---
    put:
      summary: Cập nhật thông báo
      tags:
        - Notification
      parameters:
        - name: not_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NotificationRequest'
      responses:
        200:
          description: Thông báo đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NotificationResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = notification_service.update_notification(not_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:not_id>', methods=['DELETE'])
def delete_notification(not_id):
    """
    Delete notification
    ---
    delete:
      summary: Xóa thông báo
      tags:
        - Notification
      parameters:
        - name: not_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    notification_service.delete_notification(not_id)

    return '', 204