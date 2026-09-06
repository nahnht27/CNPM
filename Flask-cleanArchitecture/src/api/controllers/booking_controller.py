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

from api.schemas.booking import (
    BookingRequestSchema,
    BookingUpdateSchema,
    BookingResponseSchema,
    ProviderBookingResponseSchema
)

from infrastructure.databases.postgres import session

from infrastructure.repositories.payment_repository import PaymentRepository


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
# PHOTOGRAPHER APIs - GIỮ API CŨ
# ==========================================================

@bp.route('/', methods=['GET'])
def list_bookings():
    photographer_id = request.args.get('photographer_id', type=int)

    try:
        items = booking_service.list_bookings()

        if photographer_id is not None:
            filtered_items = []
            for b in items:
                # 1. Bắt cả 2 trường hợp thuộc tính Python hoặc Column Name
                b_photographer_id = (
                    getattr(b, 'photographer_id', None) or 
                    getattr(b, 'PhotographerID', None)
                )

                # 2. Trường hợp Repository trả về dict thay vì Object
                if b_photographer_id is None and isinstance(b, dict):
                    b_photographer_id = b.get('photographer_id') or b.get('PhotographerID')

                # 3. So sánh sau khi ép kiểu an toàn
                if b_photographer_id is not None and int(b_photographer_id) == int(photographer_id):
                    filtered_items.append(b)

            items = filtered_items

        return jsonify(
            response_schema.dump(items, many=True)
        ), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Không thể lấy danh sách booking',
            'error': str(e)
        }), 500


@bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """
    ---
    get:
      tags:
        - Booking
      summary: Lấy thông tin booking
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Thông tin booking
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        404:
          description: Không tìm thấy booking
        500:
          description: Không thể lấy booking
    """

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


@bp.route('/', methods=['POST'])
def create_booking():
    """
    ---
    post:
      tags:
        - Booking
      summary: Tạo booking mới
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        201:
          description: Tạo booking thành công
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Dữ liệu booking không hợp lệ
        500:
          description: Không thể tạo booking
    """

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
    """
    ---
    put:
      tags:
        - Booking
      summary: Cập nhật booking
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingUpdate'
      responses:
        200:
          description: Cập nhật booking thành công
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Dữ liệu booking không hợp lệ
        404:
          description: Không tìm thấy booking
        500:
          description: Không thể cập nhật booking
    """

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
    """
    ---
    delete:
      tags:
        - Booking
      summary: Xóa booking
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Xóa booking thành công
        404:
          description: Không tìm thấy booking
        500:
          description: Không thể xóa booking
    """

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
    """
    ---
    get:
      tags:
        - Booking
      summary: Lấy danh sách booking của Provider
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
        - name: status
          in: query
          required: false
          schema:
            type: string
            enum:
              - pending
              - confirmed
              - cancelled
              - checked_in
              - completed
        - name: date
          in: query
          required: false
          schema:
            type: string
        - name: space_id
          in: query
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Danh sách booking của Provider
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/BookingResponse'
        400:
          description: Trạng thái booking không hợp lệ
        500:
          description: Không thể lấy danh sách booking
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

        session.rollback()

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
    ---
    get:
      tags:
        - Booking
      summary: Lấy chi tiết booking của Provider
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết booking
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        404:
          description: Booking không tồn tại hoặc không thuộc Provider
        500:
          description: Không thể lấy chi tiết booking
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

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy chi tiết booking',
            'error': str(e)
        }), 500


# ==========================================================
# CONFIRM
# ==========================================================

@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/confirm',
    methods=['POST']
)
def confirm_provider_booking(
    provider_id,
    booking_id
):
    """
    ---
    post:
      tags:
        - Booking
      summary: Provider xác nhận booking
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Booking đã được xác nhận
        400:
          description: Không thể xác nhận booking
        404:
          description: Booking không tồn tại hoặc không thuộc Provider
        500:
          description: Không thể xác nhận booking
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


# ==========================================================
# REJECT
# ==========================================================

@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/reject',
    methods=['POST']
)
def reject_provider_booking(
    provider_id,
    booking_id
):
    """
    ---
    post:
      tags:
        - Booking
      summary: Provider từ chối booking
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Booking đã bị từ chối
        400:
          description: Không thể từ chối booking
        404:
          description: Booking không tồn tại hoặc không thuộc Provider
        500:
          description: Không thể từ chối booking
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


# ==========================================================
# CHECK-IN
# ==========================================================

@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/check-in',
    methods=['POST']
)
def check_in_provider_booking(
    provider_id,
    booking_id
):
    """
    ---
    post:
      tags:
        - Booking
      summary: Provider check-in booking
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Check-in thành công
        400:
          description: Không thể check-in booking
        404:
          description: Booking không tồn tại hoặc không thuộc Provider
        500:
          description: Không thể check-in booking
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


# ==========================================================
# CHECK-OUT
# ==========================================================

@bp.route(
    '/provider/<int:provider_id>/<int:booking_id>/check-out',
    methods=['POST']
)
def check_out_provider_booking(
    provider_id,
    booking_id
):
    """
    ---
    post:
      tags:
        - Booking
      summary: Provider check-out booking
      parameters:
        - name: provider_id
          in: path
          required: true
          schema:
            type: integer
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Check-out thành công
        400:
          description: Không thể check-out booking
        404:
          description: Booking không tồn tại hoặc không thuộc Provider
        500:
          description: Không thể check-out booking
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

