from flask import Blueprint, request, jsonify
from services.booking_service import BookingService
from infrastructure.repositories.booking_repository import BookingRepository
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('booking', __name__, url_prefix='/bookings')

booking_service = BookingService(BookingRepository(session))

request_schema = BookingRequestSchema()
response_schema = BookingResponseSchema()


@bp.route('/', methods=['GET'])
def list_bookings():
    """
    List bookings
    ---
    get:
      summary: Lấy danh sách booking
      tags:
        - Booking
      responses:
        200:
          description: Danh sách booking
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/BookingResponse'
    """
    items = booking_service.list_bookings()
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """
    Get booking
    ---
    get:
      summary: Lấy chi tiết 1 booking
      tags:
        - Booking
      parameters:
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
          description: Không tìm thấy booking
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = booking_service.get_booking(booking_id)
    if not item:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_booking():
    """
    Create booking
    ---
    post:
      summary: Tạo booking mới
      tags:
        - Booking
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        201:
          description: Booking đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = booking_service.create_booking(**data)
    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """
    Update booking
    ---
    put:
      summary: Cập nhật booking
      tags:
        - Booking
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
              $ref: '#/components/schemas/BookingRequest'
      responses:
        200:
          description: Booking đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    item = booking_service.update_booking(booking_id, **data)
    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """
    Delete booking
    ---
    delete:
      summary: Xoá booking
      tags:
        - Booking
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xoá thành công
    """
    booking_service.delete_booking(booking_id)
    return '', 204