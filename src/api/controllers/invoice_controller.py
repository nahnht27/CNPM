from flask import Blueprint, request, jsonify
from services.invoice_service import InvoiceService
from infrastructure.repositories.invoice_repository import InvoiceRepository
from api.schemas.invoice import InvoiceRequestSchema, InvoiceResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('invoice', __name__, url_prefix='/invoices')

invoice_service = InvoiceService(InvoiceRepository(session))

request_schema = InvoiceRequestSchema()
response_schema = InvoiceResponseSchema()


@bp.route('/', methods=['GET'])
def list_invoices():
    """
    List invoices
    ---
    get:
      summary: Lấy danh sách hóa đơn
      tags:
        - Invoice
      responses:
        200:
          description: Danh sách hóa đơn
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/InvoiceResponse'
    """
    items = invoice_service.list_invoices()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:inv_id>', methods=['GET'])
def get_invoice(inv_id):
    """
    Get invoice
    ---
    get:
      summary: Lấy chi tiết hóa đơn
      tags:
        - Invoice
      parameters:
        - name: inv_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết hóa đơn
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        404:
          description: Không tìm thấy hóa đơn
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = invoice_service.get_invoice(inv_id)

    if not item:
        return jsonify({'message': 'Invoice not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_invoice():
    """
    Create invoice
    ---
    post:
      summary: Tạo hóa đơn mới
      tags:
        - Invoice
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceRequest'
      responses:
        201:
          description: Hóa đơn đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = invoice_service.create_invoice(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:inv_id>', methods=['PUT'])
def update_invoice(inv_id):
    """
    Update invoice
    ---
    put:
      summary: Cập nhật hóa đơn
      tags:
        - Invoice
      parameters:
        - name: inv_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceRequest'
      responses:
        200:
          description: Hóa đơn đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = invoice_service.update_invoice(inv_id, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:inv_id>', methods=['DELETE'])
def delete_invoice(inv_id):
    """
    Delete invoice
    ---
    delete:
      summary: Xóa hóa đơn
      tags:
        - Invoice
      parameters:
        - name: inv_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    invoice_service.delete_invoice(inv_id)

    return '', 204