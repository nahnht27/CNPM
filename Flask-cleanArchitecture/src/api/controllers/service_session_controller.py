from flask import Blueprint, request, jsonify

from services.service_session_service import ServiceSessionService

from infrastructure.repositories.service_session_repository import (
    ServiceSessionRepository
)

from api.schemas.service_session import (
    ServiceSessionRequestSchema,
    ServiceSessionUpdateSchema,
    ServiceSessionResponseSchema
)

from infrastructure.databases.postgres import session


bp = Blueprint(
    'service_session',
    __name__,
    url_prefix='/service-sessions'
)


# ==========================================================
# SERVICE
# ==========================================================

service = ServiceSessionService(
    ServiceSessionRepository(session)
)


# ==========================================================
# SCHEMAS
# ==========================================================

request_schema = ServiceSessionRequestSchema()
update_schema = ServiceSessionUpdateSchema()
response_schema = ServiceSessionResponseSchema()


# ==========================================================
# GET ALL
# ==========================================================

@bp.route('/', methods=['GET'])
def list_sessions():

    try:
        items = service.list_sessions()

        return jsonify(
            response_schema.dump(
                items,
                many=True
            )
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy danh sách ServiceSession',
            'error': str(e)
        }), 500


# ==========================================================
# GET BY ID
# ==========================================================

@bp.route('/<int:session_id>', methods=['GET'])
def get_session(session_id):

    try:

        item = service.get_session(
            session_id
        )

        if not item:
            return jsonify({
                'message': 'ServiceSession not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy ServiceSession',
            'error': str(e)
        }), 500


# ==========================================================
# GET BY BOOKING
# ==========================================================

@bp.route(
    '/booking/<int:booking_id>',
    methods=['GET']
)
def get_session_by_booking(booking_id):

    try:

        item = service.get_session_by_booking(
            booking_id
        )

        if not item:
            return jsonify({
                'message': 'ServiceSession not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message':
                'Không thể lấy ServiceSession theo booking',
            'error': str(e)
        }), 500


# ==========================================================
# CREATE
# ==========================================================

@bp.route('/', methods=['POST'])
def create_session():

    data = request.get_json() or {}

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:

        cleaned_data = request_schema.load(data)

        item = service.create_session(
            **cleaned_data
        )

        return jsonify(
            response_schema.dump(item)
        ), 201

    except ValueError as e:

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message':
                'Không thể tạo ServiceSession',
            'error': str(e)
        }), 500


# ==========================================================
# CHECK-IN
# ==========================================================

@bp.route(
    '/booking/<int:booking_id>/check-in',
    methods=['POST']
)
def check_in(booking_id):

    data = request.get_json() or {}

    check_in_method = data.get(
        'check_in_method'
    )

    notes = data.get(
        'notes'
    )

    try:

        item, error = service.check_in(
            booking_id=booking_id,
            check_in_method=check_in_method,
            notes=notes
        )

        if error:
            return jsonify({
                'message': error
            }), 400

        return jsonify({
            'message': 'Check-in thành công',
            'service_session':
                response_schema.dump(item)
        }), 200

    except ValueError as e:

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể check-in',
            'error': str(e)
        }), 500


# ==========================================================
# CHECK-OUT
# ==========================================================

@bp.route(
    '/booking/<int:booking_id>/check-out',
    methods=['POST']
)
def check_out(booking_id):

    data = request.get_json() or {}

    notes = data.get(
        'notes'
    )

    try:

        item, error = service.check_out(
            booking_id=booking_id,
            notes=notes
        )

        if error:
            return jsonify({
                'message': error
            }), 400

        return jsonify({
            'message': 'Check-out thành công',
            'service_session':
                response_schema.dump(item)
        }), 200

    except ValueError as e:

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể check-out',
            'error': str(e)
        }), 500


# ==========================================================
# UPDATE
# ==========================================================

@bp.route(
    '/<int:session_id>',
    methods=['PUT']
)
def update_session(session_id):

    data = request.get_json() or {}

    errors = update_schema.validate(
        data,
        partial=True
    )

    if errors:
        return jsonify(errors), 400

    try:

        cleaned_data = update_schema.load(
            data,
            partial=True
        )

        item = service.update_session(
            session_id,
            **cleaned_data
        )

        if not item:
            return jsonify({
                'message': 'ServiceSession not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except ValueError as e:

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message':
                'Không thể cập nhật ServiceSession',
            'error': str(e)
        }), 500


# ==========================================================
# DELETE
# ==========================================================

@bp.route(
    '/<int:session_id>',
    methods=['DELETE']
)
def delete_session(session_id):

    try:

        deleted = service.delete_session(
            session_id
        )

        if not deleted:
            return jsonify({
                'message': 'ServiceSession not found'
            }), 404

        return '', 204

    except Exception as e:

        session.rollback()

        return jsonify({
            'message':
                'Không thể xóa ServiceSession',
            'error': str(e)
        }), 500