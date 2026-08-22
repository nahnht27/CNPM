from flask import Blueprint, request, jsonify
from services.complaint_service import ComplaintService
from infrastructure.repositories.complaint_repository import ComplaintRepository
from api.schemas.complaint import ComplaintRequestSchema, ComplaintResponseSchema
from infrastructure.databases.mssql import session

bp = Blueprint('complaint', __name__, url_prefix='/complaints')

complaint_service = ComplaintService(ComplaintRepository(session))

request_schema = ComplaintRequestSchema()
response_schema = ComplaintResponseSchema()


@bp.route('/', methods=['GET'])
def list_complaints():
    """
    List complaints
    ---
    get:
      summary: Lấy danh sách khiếu nại
      tags:
        - Complaint
      responses:
        200:
          description: Danh sách khiếu nại
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ComplaintResponse'
    """
    items = complaint_service.list_complaints()

    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route('/<int:cid>', methods=['GET'])
def get_complaint(cid):
    """
    Get complaint
    ---
    get:
      summary: Lấy chi tiết khiếu nại
      tags:
        - Complaint
      parameters:
        - name: cid
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết khiếu nại
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ComplaintResponse'
        404:
          description: Không tìm thấy khiếu nại
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    item = complaint_service.get_complaint(cid)

    if not item:
        return jsonify({'message': 'Complaint not found'}), 404

    return jsonify(response_schema.dump(item)), 200


@bp.route('/', methods=['POST'])
def create_complaint():
    """
    Create complaint
    ---
    post:
      summary: Tạo khiếu nại mới
      tags:
        - Complaint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ComplaintRequest'
      responses:
        201:
          description: Khiếu nại đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ComplaintResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = complaint_service.create_complaint(**data)

    return jsonify(response_schema.dump(item)), 201


@bp.route('/<int:cid>', methods=['PUT'])
def update_complaint(cid):
    """
    Update complaint
    ---
    put:
      summary: Cập nhật khiếu nại
      tags:
        - Complaint
      parameters:
        - name: cid
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ComplaintRequest'
      responses:
        200:
          description: Khiếu nại đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ComplaintResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    data = request.get_json()

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    item = complaint_service.update_complaint(cid, **data)

    return jsonify(response_schema.dump(item)), 200


@bp.route('/<int:cid>', methods=['DELETE'])
def delete_complaint(cid):
    """
    Delete complaint
    ---
    delete:
      summary: Xóa khiếu nại
      tags:
        - Complaint
      parameters:
        - name: cid
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    complaint_service.delete_complaint(cid)

    return '', 204