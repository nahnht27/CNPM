from flask import Blueprint, request, jsonify

from services.payment_service import PaymentService

from infrastructure.repositories.payment_repository import (
    PaymentRepository
)

from infrastructure.repositories.invoice_repository import (
    InvoiceRepository
)

from api.schemas.payment import (
    PaymentRequestSchema,
    PaymentResponseSchema
)

from infrastructure.databases.postgres import session


bp = Blueprint(
    'payment',
    __name__,
    url_prefix='/payments'
)


# ==========================================================
# SERVICES
# ==========================================================

payment_service = PaymentService(
    PaymentRepository(session),
    InvoiceRepository(session)
)


request_schema = PaymentRequestSchema()
response_schema = PaymentResponseSchema()


# ==========================================================
# GET ALL
# ==========================================================

@bp.route('/', methods=['GET'])
def list_payments():

    try:

        items = payment_service.list_payments()

        return jsonify(
            response_schema.dump(
                items,
                many=True
            )
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy danh sách thanh toán',
            'error': str(e)
        }), 500


# ==========================================================
# GET BY ID
# ==========================================================

@bp.route('/<int:pay_id>', methods=['GET'])
def get_payment(pay_id):

    try:

        item = payment_service.get_payment(
            pay_id
        )

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


# ==========================================================
# GET BY INVOICE
# ==========================================================

@bp.route(
    '/invoice/<int:invoice_id>',
    methods=['GET']
)
def get_payment_by_invoice(invoice_id):

    try:

        item = payment_service.get_payment_by_invoice(
            invoice_id
        )

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
            'message':
                'Không thể lấy thanh toán theo Invoice',
            'error': str(e)
        }), 500


# ==========================================================
# CREATE
# ==========================================================

@bp.route('/', methods=['POST'])
def create_payment():

    data = request.get_json() or {}

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

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể tạo thanh toán',
            'error': str(e)
        }), 500


# ==========================================================
# UPDATE
# ==========================================================

@bp.route('/<int:pay_id>', methods=['PUT'])
def update_payment(pay_id):

    data = request.get_json() or {}

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:

        cleaned_data = request_schema.load(data)

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

        return jsonify({
            'message': str(e)
        }), 400

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể cập nhật thanh toán',
            'error': str(e)
        }), 500


# ==========================================================
# DELETE
# ==========================================================

@bp.route('/<int:pay_id>', methods=['DELETE'])
def delete_payment(pay_id):

    try:

        deleted = payment_service.delete_payment(
            pay_id
        )

        if not deleted:
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