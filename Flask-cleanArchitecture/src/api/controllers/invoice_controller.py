from flask import Blueprint, request, jsonify

from services.invoice_service import InvoiceService
from infrastructure.repositories.invoice_repository import InvoiceRepository
from api.schemas.invoice import (
    InvoiceRequestSchema,
    InvoiceResponseSchema
)

from infrastructure.databases.postgres import session


bp = Blueprint(
    'invoice',
    __name__,
    url_prefix='/invoices'
)


invoice_service = InvoiceService(
    InvoiceRepository(session)
)


request_schema = InvoiceRequestSchema()
response_schema = InvoiceResponseSchema()


# ==========================================================
# GET ALL
# ==========================================================

@bp.route('/', methods=['GET'])
def list_invoices():

    try:

        items = invoice_service.list_invoices()

        return jsonify(
            response_schema.dump(
                items,
                many=True
            )
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy danh sách hóa đơn',
            'error': str(e)
        }), 500


# ==========================================================
# GET BY ID
# ==========================================================

@bp.route('/<int:inv_id>', methods=['GET'])
def get_invoice(inv_id):

    try:

        item = invoice_service.get_invoice(inv_id)

        if not item:
            return jsonify({
                'message': 'Invoice not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể lấy hóa đơn',
            'error': str(e)
        }), 500


# ==========================================================
# GET BY SERVICE SESSION
# ==========================================================

@bp.route('/session/<int:session_id>', methods=['GET'])
def get_invoice_by_session(session_id):

    try:

        item = invoice_service.get_invoice_by_session(
            session_id
        )

        if not item:
            return jsonify({
                'message': 'Invoice not found'
            }), 404

        return jsonify(
            response_schema.dump(item)
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message':
                'Không thể lấy hóa đơn theo ServiceSession',
            'error': str(e)
        }), 500


# ==========================================================
# CREATE
# ==========================================================

@bp.route('/', methods=['POST'])
def create_invoice():

    data = request.get_json() or {}

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:

        cleaned_data = request_schema.load(data)

        item = invoice_service.create_invoice(
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
            'message': 'Không thể tạo hóa đơn',
            'error': str(e)
        }), 500


# ==========================================================
# UPDATE
# ==========================================================

@bp.route('/<int:inv_id>', methods=['PUT'])
def update_invoice(inv_id):

    data = request.get_json() or {}

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:

        cleaned_data = request_schema.load(data)

        item = invoice_service.update_invoice(
            inv_id,
            **cleaned_data
        )

        if not item:
            return jsonify({
                'message': 'Invoice not found'
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
            'message': 'Không thể cập nhật hóa đơn',
            'error': str(e)
        }), 500


# ==========================================================
# DELETE
# ==========================================================

@bp.route('/<int:inv_id>', methods=['DELETE'])
def delete_invoice(inv_id):

    try:

        deleted = invoice_service.delete_invoice(
            inv_id
        )

        if not deleted:
            return jsonify({
                'message': 'Invoice not found'
            }), 404

        return '', 204

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': 'Không thể xóa hóa đơn',
            'error': str(e)
        }), 500