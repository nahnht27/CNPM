from flask import Blueprint, request, jsonify, session

from services.workshop_registration_service import WorkshopRegistrationService
from infrastructure.repositories.workshop_registration_repository import (
    WorkshopRegistrationRepository
)
from infrastructure.repositories.workshop_repository import WorkshopRepository

from api.schemas.workshop_registration import (
    WorkshopRegistrationRequestSchema,
    WorkshopRegistrationResponseSchema
)

from infrastructure.databases.factory_database import FactoryDatabase as db_factory


bp = Blueprint(
    'workshop_registration',
    __name__,
    url_prefix='/workshop-registrations'
)


registration_repository = WorkshopRegistrationRepository(session)
workshop_repository = WorkshopRepository(session)

workshop_registration_service = WorkshopRegistrationService(
    registration_repository,
    workshop_repository
)

request_schema = WorkshopRegistrationRequestSchema()
response_schema = WorkshopRegistrationResponseSchema()


@bp.route('/', methods=['POST'])
def register_workshop():
    """
    Register workshop
    ---
    post:
      summary: Photographer đăng ký workshop
      tags:
        - Workshop Registration
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkshopRegistrationRequest'
      responses:
        201:
          description: Đăng ký workshop thành công
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkshopRegistrationResponse'
        400:
          description: Dữ liệu không hợp lệ
        404:
          description: Không tìm thấy workshop
        409:
          description: Đã đăng ký hoặc workshop đã đầy
    """

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Request body is required'
        }), 400

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        registration = workshop_registration_service.register(
            workshop_id=data['workshop_id'],
            user_id=data['user_id']
        )

        return jsonify(
            response_schema.dump(registration)
        ), 201

    except ValueError as e:
        message = str(e)

        if message == 'Workshop not found':
            return jsonify({
                'message': message
            }), 404

        return jsonify({
            'message': message
        }), 409


@bp.route('/user/<int:user_id>', methods=['GET'])
def list_user_registrations(user_id):
    """
    List user's workshop registrations
    ---
    get:
      summary: Lấy danh sách workshop đã đăng ký
      tags:
        - Workshop Registration
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Danh sách workshop đã đăng ký
    """

    registrations = workshop_registration_service.list_by_user(
        user_id
    )

    return jsonify(
        response_schema.dump(registrations, many=True)
    ), 200


@bp.route('/workshop/<int:workshop_id>', methods=['GET'])
def list_workshop_registrations(workshop_id):
    """
    List workshop registrations
    ---
    get:
      summary: Lấy danh sách người đăng ký workshop
      tags:
        - Workshop Registration
      parameters:
        - name: workshop_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Danh sách đăng ký
    """

    registrations = workshop_registration_service.list_by_workshop(
        workshop_id
    )

    return jsonify(
        response_schema.dump(registrations, many=True)
    ), 200