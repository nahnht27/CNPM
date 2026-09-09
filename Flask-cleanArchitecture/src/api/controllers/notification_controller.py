from flask import Blueprint, request, jsonify

from services.notification_service import NotificationService
from infrastructure.repositories.notification_repository import NotificationRepository
from api.schemas.notification import (
    NotificationRequestSchema,
    NotificationResponseSchema
)
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


bp = Blueprint('notification', __name__, url_prefix='/notifications')


notification_service = NotificationService(
    NotificationRepository(
        db_factory.get_database('POSTGREE').session
    )
)

request_schema = NotificationRequestSchema()
response_schema = NotificationResponseSchema()


@bp.route('/', methods=['GET'])
def list_notifications():
    items = notification_service.list_notifications()
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/user/<int:user_id>', methods=['GET'])
def list_user_notifications(user_id):
    items = notification_service.list_user_notifications(user_id)
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/user/<int:user_id>/unread-count', methods=['GET'])
def unread_count(user_id):
    count = notification_service.count_unread(user_id)
    return jsonify({'count': count}), 200


@bp.route('/<int:not_id>', methods=['GET'])
def get_notification(not_id):
    item = notification_service.get_notification(not_id)

    if not item:
        return jsonify({
            'message': 'Notification not found'
        }), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:not_id>/read', methods=['PUT'])
def mark_notification_as_read(not_id):
    item = notification_service.mark_as_read(not_id)

    if not item:
        return jsonify({
            'message': 'Notification not found'
        }), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_notification():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Request body is required'
        }), 400

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = notification_service.create_notification(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:not_id>', methods=['PUT'])
def update_notification(not_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Request body is required'
        }), 400

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        item = notification_service.update_notification(
            not_id,
            **data
        )

        return jsonify(response_schema.dump(item)), 200

    except ValueError as e:
        return jsonify({
            'message': str(e)
        }), 404


@bp.route('/<int:not_id>', methods=['DELETE'])
def delete_notification(not_id):
    notification_service.delete_notification(not_id)
    return '', 204