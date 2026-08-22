from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService
from infrastructure.repositories.payment_repository import PaymentRepository
from api.schemas.payment import PaymentRequestSchema, PaymentResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('payment', __name__, url_prefix='/payments')

payment_service = PaymentService(PaymentRepository(session))

request_schema = PaymentRequestSchema()
response_schema = PaymentResponseSchema()


@bp.route('/', methods=['GET'])
def list_payments():
    """
    List payments
    ---
    get:
      summary: Lấy danh sách thanh toán
      tags:
        - Payment
      responses:
        200:
          description: Danh sách thanh toán
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PaymentResponse'
    """
    items = payment_service.list_payments()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:pay_id>', methods=['GET'])
def get_payment(pay_id):
    """
    Get payment
    ---
    get:
      summary: Lấy chi tiết thanh toán
      tags:
        - Payment
      parameters:
        - name: pay_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết thanh toán
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'
        404:
          description: Không tìm thấy thanh toán
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = payment_service.get_payment(pay_id)

    if not item:
        return jsonify({'message': 'Payment not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_payment():
    """
    Create payment
    ---
    post:
      summary: Tạo thanh toán mới
      tags:
        - Payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentRequest'
      responses:
        201:
          description: Thanh toán đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = payment_service.create_payment(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:pay_id>', methods=['PUT'])
def update_payment(pay_id):
    """
    Update payment
    ---
    put:
      summary: Cập nhật thanh toán
      tags:
        - Payment
      parameters:
        - name: pay_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentRequest'
      responses:
        200:
          description: Thanh toán đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = payment_service.update_payment(pay_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:pay_id>', methods=['DELETE'])
def delete_payment(pay_id):
    """
    Delete payment
    ---
    delete:
      summary: Xóa thanh toán
      tags:
        - Payment
      parameters:
        - name: pay_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    payment_service.delete_payment(pay_id)

    return '', 204