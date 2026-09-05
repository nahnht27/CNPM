from flask import Blueprint, request, jsonify

from services.booking_service import BookingService
from infrastructure.repositories.booking_repository import BookingRepository
from api.schemas.booking import (
    BookingRequestSchema,
    BookingUpdateSchema,
    BookingResponseSchema,
    ProviderBookingResponseSchema
)
from infrastructure.databases.postgres import session


bp = Blueprint(
    'booking',
    __name__,
    url_prefix='/bookings'
)

booking_service = BookingService(
    BookingRepository(session)
)

request_schema = BookingRequestSchema()
update_schema = BookingUpdateSchema()
response_schema = BookingResponseSchema()
provider_response_schema = ProviderBookingResponseSchema()


# ==========================================================
# PHOTOGRAPHER APIs - GIỮ API CŨ
# ==========================================================

@bp.route('/', methods=['GET'])
def list_bookings():
    photographer_id = request.args.get(
        'photographer_id',
        type=int
    )

    items = booking_service.list_bookings()

    if photographer_id:
        items = [
            b for b in items
            if getattr(b, 'photographer_id', None) == photographer_id
        ]

    return jsonify(
        response_schema.dump(items, many=True)
    ), 200


@bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    item = booking_service.get_booking(booking_id)

    if not item:
        return jsonify({
            'message': 'Booking not found'
        }), 404

    return jsonify(
        response_schema.dump(item)
    ), 200


@bp.route('/', methods=['POST'])
def create_booking():
    data = request.get_json() or {}

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        cleaned_data = request_schema.load(data)
        item = booking_service.create_booking(**cleaned_data)

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
            'message': 'Không thể tạo booking',
            'error': str(e)
        }), 500


@bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
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

        item = booking_service.update_booking(
            booking_id,
            **cleaned_data
        )

        if not item:
            return jsonify({
                'message': 'Booking not found'
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
            'message': 'Không thể cập nhật booking',
            'error': str(e)
        }), 500


@bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    deleted = booking_service.delete_booking(
        booking_id
    )

    if not deleted:
        return jsonify({
            'message': 'Booking not found'
        }), 404

    return '', 204


# ==========================================================
# PROVIDER BOOKING MANAGEMENT
# ==========================================================

@bp.route('/provider/<int:provider_id>', methods=['GET'])
def get_provider_bookings(provider_id):
    """
    Lấy danh sách booking thuộc provider.
    """

    status = request.args.get(
        'status',
        type=str
    )

    date = request.args.get(
        'date',
        type=str
    )

    space_id = request.args.get(
        'space_id',
        type=int
    )

    allowed_statuses = {
        'pending',
        'confirmed',
        'cancelled',
        'checked_in',
        'completed'
    }

    if status and status not in allowed_statuses:
        return jsonify({
            'message': 'Trạng thái booking không hợp lệ'
        }), 400

    try:
        items = booking_service.list_provider_bookings(
            provider_id=provider_id,
            status=status,
            date=date,
            space_id=space_id
        )

        return jsonify(
            provider_response_schema.dump(
                items,
                many=True
            )
        ), 200

    except Exception as e:
        return jsonify({
            'message': 'Không thể lấy danh sách booking',
            'error': str(e)
        }), 500


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>',
    methods=['GET']
)
def get_provider_booking(
    provider_id,
    booking_id
):
    """
    Lấy chi tiết booking thuộc provider.
    """

    try:
        item = booking_service.get_provider_booking(
            provider_id,
            booking_id
        )

        if not item:
            return jsonify({
                'message': (
                    'Booking không tồn tại '
                    'hoặc không thuộc provider này'
                )
            }), 404

        return jsonify(
            provider_response_schema.dump(item)
        ), 200

    except Exception as e:
        return jsonify({
            'message': 'Không thể lấy chi tiết booking',
            'error': str(e)
        }), 500


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/confirm',
    methods=['POST']
)
def confirm_provider_booking(
    provider_id,
    booking_id
):
    """
    Provider xác nhận booking.
    """

    try:
        item, error = booking_service.confirm_booking(
            provider_id,
            booking_id
        )

        if error:
            status_code = 404 if not item else 400

            return jsonify({
                'message': error
            }), status_code

        return jsonify({
            'message': 'Booking đã được xác nhận',
            'booking': provider_response_schema.dump(item)
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể xác nhận booking',
            'error': str(e)
        }), 500


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/reject',
    methods=['POST']
)
def reject_provider_booking(
    provider_id,
    booking_id
):
    """
    Provider từ chối booking.
    """

    try:
        item, error = booking_service.reject_booking(
            provider_id,
            booking_id
        )

        if error:
            status_code = 404 if not item else 400

            return jsonify({
                'message': error
            }), status_code

        return jsonify({
            'message': 'Booking đã bị từ chối',
            'booking': provider_response_schema.dump(item)
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể từ chối booking',
            'error': str(e)
        }), 500


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/check-in',
    methods=['POST']
)
def check_in_provider_booking(
    provider_id,
    booking_id
):
    """
    Provider check-in booking.
    """

    try:
        item, error = booking_service.check_in_booking(
            provider_id,
            booking_id
        )

        if error:
            status_code = 404 if not item else 400

            return jsonify({
                'message': error
            }), status_code

        return jsonify({
            'message': 'Check-in thành công',
            'booking': provider_response_schema.dump(item)
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể check-in booking',
            'error': str(e)
        }), 500


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/check-out',
    methods=['POST']
)
def check_out_provider_booking(
    provider_id,
    booking_id
):
    """
    Provider check-out booking.
    """

    try:
        item, error = booking_service.check_out_booking(
            provider_id,
            booking_id
        )

        if error:
            status_code = 404 if not item else 400

            return jsonify({
                'message': error
            }), status_code

        return jsonify({
            'message': 'Check-out thành công',
            'booking': provider_response_schema.dump(item)
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể check-out booking',
            'error': str(e)
        }), 500
