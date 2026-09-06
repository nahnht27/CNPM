
from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService
from infrastructure.repositories.payment_repository import PaymentRepository
from api.schemas.payment import (
    PaymentRequestSchema,
    PaymentUpdateSchema,
    PaymentResponseSchema
)
from infrastructure.databases.factory_database import FactoryDatabase


bp = Blueprint(
    'payment',
    __name__,
    url_prefix='/payments'
)


# ============================================================
# DATABASE
# ============================================================

db = FactoryDatabase.get_database('POSTGREE')
session = db.session


# ============================================================
# SERVICE
# ============================================================

payment_service = PaymentService(
    PaymentRepository(session)
)


# ============================================================
# SCHEMAS
# ============================================================

request_schema = PaymentRequestSchema()
update_schema = PaymentUpdateSchema()
response_schema = PaymentResponseSchema()


# ============================================================
# GET ALL PAYMENTS
# ============================================================

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

    try:
        items = payment_service.list_payments()

        return jsonify(
            response_schema.dump(items, many=True)
        ), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể lấy danh sách thanh toán',
            'error': str(e)
        }), 500


# ============================================================
# GET PAYMENT BY ID
# ============================================================

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
    """

    try:
        item = payment_service.get_payment(pay_id)

        if not item:
            return jsonify({
                'message': 'Payment not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể lấy thanh toán',
            'error': str(e)
        }), 500


# ============================================================
# CREATE PAYMENT
# ============================================================

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
        500:
          description: Lỗi server
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'message': 'Request body phải là JSON object'
        }), 400

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        cleaned_data = request_schema.load(data)

        item = payment_service.create_payment(
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
            'message': 'Không thể tạo thanh toán',
            'error': str(e)
        }), 500


# ============================================================
# GET PAYMENT BY INVOICE
# ============================================================

@bp.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_payment_by_invoice(invoice_id):
    """
    Get payment by invoice
    ---
    get:
      summary: Lấy thanh toán theo Invoice
      tags:
        - Payment
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Thông tin thanh toán
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'
        404:
          description: Không tìm thấy thanh toán
    """

    try:
        item = payment_service.get_payment_by_invoice(
            invoice_id
        )

        if not item:
            return jsonify({
                'message': 'Payment not found for this invoice'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể lấy thanh toán theo invoice',
            'error': str(e)
        }), 500


# ============================================================
# UPDATE PAYMENT STATUS
# ============================================================

@bp.route('/<int:pay_id>', methods=['PUT'])
def update_payment(pay_id):
    """
    Update payment status
    ---
    put:
      summary: Cập nhật trạng thái thanh toán
      description: |
        Provider sử dụng API này để xác nhận trạng thái thanh toán.
        Không cần gửi invoice_id, amount hoặc payment_method.
      tags:
        - Payment

      parameters:
        - name: pay_id
          in: path
          required: true
          description: ID của Payment
          schema:
            type: integer

      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - status
              properties:
                status:
                  type: string
                  enum:
                    - Đang chờ xử lý
                    - Thành công
                    - Thất bại
                    - Đã hoàn tiền
                  example: Thành công

      responses:
        200:
          description: Thanh toán đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponse'

        400:
          description: Dữ liệu không hợp lệ

        404:
          description: Không tìm thấy thanh toán

        500:
          description: Lỗi server
    """

    data = request.get_json(silent=True)

    # PUT bắt buộc phải nhận JSON object
    if not isinstance(data, dict):
        return jsonify({
            'message': 'Request body phải là JSON object',
            'example': {
                'status': 'Thành công'
            }
        }), 400

    errors = update_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        cleaned_data = update_schema.load(data)

        item = payment_service.update_payment(
            pay_id,
            **cleaned_data
        )

        if not item:
            return jsonify({
                'message': 'Payment not found'
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
            'message': 'Không thể cập nhật thanh toán',
            'error': str(e)
        }), 500


# ============================================================
# DELETE PAYMENT
# ============================================================

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
        404:
          description: Không tìm thấy thanh toán
    """

    try:
        result = payment_service.delete_payment(pay_id)

        if not result:
            return jsonify({
                'message': 'Payment not found'
            }), 404

        return '', 204

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Không thể xóa thanh toán',
            'error': str(e)
        }), 500

