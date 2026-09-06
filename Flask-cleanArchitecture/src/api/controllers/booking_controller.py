from flask import Blueprint, request, jsonify

from services.booking_service import BookingService

from infrastructure.repositories.booking_repository import (
    BookingRepository
)

from infrastructure.repositories.service_session_repository import (
    ServiceSessionRepository
)

from infrastructure.repositories.invoice_repository import (
    InvoiceRepository
)

from infrastructure.repositories.payment_repository import (
    PaymentRepository
)

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


# ==========================================================
# SERVICE
# ==========================================================

booking_service = BookingService(
    BookingRepository(session),
    ServiceSessionRepository(session),
    InvoiceRepository(session),
    PaymentRepository(session)
)


request_schema = BookingRequestSchema()
update_schema = BookingUpdateSchema()
response_schema = BookingResponseSchema()
provider_response_schema = ProviderBookingResponseSchema()


# ==========================================================
# PHOTOGRAPHER APIs
# ==========================================================


@bp.route('/', methods=['GET'])
def list_bookings():

    photographer_id = request.args.get(
        'photographer_id',
        type=int
    )

    try:

        items = booking_service.list_bookings()

        # Giữ nguyên logic lọc booking của Photographer
        if photographer_id:
            items = [
                b for b in items
                if getattr(
                    b,
                    'photographer_id',
                    None
                ) == photographer_id
            ]

        return jsonify(
            response_schema.dump(
                items,
                many=True
            )
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy danh sách booking',
            'error': str(e)
        }), 500


# ==========================================================
# GET BOOKING DETAIL
# ==========================================================


@bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):

    try:

        item = booking_service.get_booking(
            booking_id
        )

        if not item:
            return jsonify({
                'message': 'Booking not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy booking',
            'error': str(e)
        }), 500


# ==========================================================
# CREATE BOOKING
# ==========================================================


@bp.route('/', methods=['POST'])
def create_booking():

    data = request.get_json() or {}

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:

        cleaned_data = request_schema.load(data)

        item = booking_service.create_booking(
            **cleaned_data
        )

        return jsonify(
            response_schema.dump(item)
        ), 201

    except ValueError as e:

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể tạo booking',
            'error': str(e)
        }), 500


# ==========================================================
# UPDATE BOOKING
# ==========================================================
#
# Photographer chỉ được cập nhật thông tin booking.
#
# Không cho phép dùng PUT để bypass flow Provider:
#
# pending
#    ↓
# Provider confirm
#    ↓
# confirmed
#    ↓
# Payment
#    ↓
# Provider check-in
#    ↓
# checked_in
#    ↓
# Provider check-out
#    ↓
# completed
#
# ==========================================================


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

        # --------------------------------------------------
        # Không cho PUT thay đổi trạng thái vận hành
        # --------------------------------------------------

        forbidden_statuses = {
            'confirmed',
            'checked_in',
            'completed'
        }

        new_status = cleaned_data.get('status')

        if new_status in forbidden_statuses:

            return jsonify({
                'message': (
                    'Không thể thay đổi trạng thái '
                    f'{new_status} bằng API này. '
                    'Vui lòng sử dụng API dành cho Provider.'
                )
            }), 403

        # --------------------------------------------------
        # Chỉ cho Photographer hủy booking
        # --------------------------------------------------

        if new_status and new_status != 'cancelled':

            return jsonify({
                'message': (
                    'Trạng thái cập nhật không hợp lệ'
                )
            }), 400

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

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể cập nhật booking',
            'error': str(e)
        }), 500


# ==========================================================
# DELETE BOOKING
# ==========================================================


@bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):

    try:

        deleted = booking_service.delete_booking(
            booking_id
        )

        if not deleted:

            return jsonify({
                'message': 'Booking not found'
            }), 404

        return '', 204

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể xóa booking',
            'error': str(e)
        }), 500


# ==========================================================
# PROVIDER BOOKING MANAGEMENT
# ==========================================================


@bp.route(
    '/provider/<int:provider_id>',
    methods=['GET']
)
def get_provider_bookings(provider_id):

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

    # Các trạng thái hợp lệ của Booking
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

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy danh sách booking',
            'error': str(e)
        }), 500


# ==========================================================
# PROVIDER GET BOOKING DETAIL
# ==========================================================


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>',
    methods=['GET']
)
def get_provider_booking(
    provider_id,
    booking_id
):

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

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy chi tiết booking',
            'error': str(e)
        }), 500


# ==========================================================
# PROVIDER CONFIRM
# ==========================================================


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/confirm',
    methods=['POST']
)
def confirm_provider_booking(
    provider_id,
    booking_id
):

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


# ==========================================================
# PROVIDER REJECT
# ==========================================================


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/reject',
    methods=['POST']
)
def reject_provider_booking(
    provider_id,
    booking_id
):

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


# ==========================================================
# PROVIDER CHECK-IN
# ==========================================================


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/check-in',
    methods=['POST']
)
def check_in_provider_booking(
    provider_id,
    booking_id
):

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


# ==========================================================
# PROVIDER CHECK-OUT
# ==========================================================


@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/check-out',
    methods=['POST']
)
def check_out_provider_booking(
    provider_id,
    booking_id
):

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