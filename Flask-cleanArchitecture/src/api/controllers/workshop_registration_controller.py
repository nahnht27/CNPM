from flask import Blueprint, request, jsonify, session

from services.notification_service import NotificationService
from infrastructure.repositories.notification_repository import (
    NotificationRepository
)
from infrastructure.databases.factory_database import (
    FactoryDatabase as db_factory
)

from services.workshop_registration_service import (
    WorkshopRegistrationService
)

from infrastructure.repositories.workshop_registration_repository import (
    WorkshopRegistrationRepository
)

from infrastructure.repositories.workshop_repository import (
    WorkshopRepository
)

from api.schemas.workshop_registration import (
    WorkshopRegistrationRequestSchema,
    WorkshopRegistrationResponseSchema
)


bp = Blueprint(
    'workshop_registration',
    __name__,
    url_prefix='/workshop-registrations'
)


# =====================================================
# NOTIFICATION SERVICE
# =====================================================

notification_service = NotificationService(

    NotificationRepository(
        db_factory.get_database('POSTGREE').session
    )

)


# =====================================================
# REPOSITORIES
# =====================================================

registration_repository = WorkshopRegistrationRepository(
    session
)

workshop_repository = WorkshopRepository(
    session
)


# =====================================================
# WORKSHOP REGISTRATION SERVICE
# =====================================================

workshop_registration_service = WorkshopRegistrationService(

    registration_repository,

    workshop_repository,

    notification_service

)


# =====================================================
# SCHEMAS
# =====================================================

request_schema = WorkshopRegistrationRequestSchema()

response_schema = WorkshopRegistrationResponseSchema()


# =====================================================
# REGISTER WORKSHOP
# =====================================================

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
        400:
          description: Dữ liệu không hợp lệ
        404:
          description: Không tìm thấy workshop
        409:
          description: Đã đăng ký hoặc workshop đã đầy
    """

    data = request.get_json()


    # =================================================
    # Check request body
    # =================================================

    if not data:

        return jsonify({
            'message': 'Request body is required'
        }), 400


    # =================================================
    # Validate request
    # =================================================

    errors = request_schema.validate(
        data
    )

    if errors:

        return jsonify(errors), 400


    # =================================================
    # Register
    # =================================================

    try:

        registration = (
            workshop_registration_service.register(

                workshop_id=data['workshop_id'],

                user_id=data['user_id']

            )
        )


        return jsonify(
            response_schema.dump(
                registration
            )
        ), 201


    except ValueError as e:

        message = str(e)


        # Workshop not found

        if message == 'Workshop not found':

            return jsonify({
                'message': message
            }), 404


        # Duplicate / full

        return jsonify({
            'message': message
        }), 409


# =====================================================
# LIST USER REGISTRATIONS
# =====================================================

@bp.route('/user/<int:user_id>', methods=['GET'])
def list_user_registrations(user_id):
    """
    List user's workshop registrations
    """

    registrations = (
        workshop_registration_service
        .list_by_user(
            user_id
        )
    )


    return jsonify(

        response_schema.dump(

            registrations,

            many=True

        )

    ), 200


# =====================================================
# LIST WORKSHOP REGISTRATIONS
# =====================================================

@bp.route(
    '/workshop/<int:workshop_id>',
    methods=['GET']
)
def list_workshop_registrations(workshop_id):
    """
    List workshop registrations
    """

    # =================================================
    # Check workshop exists
    # =================================================

    workshop = (
        workshop_repository
        .get_by_id(
            workshop_id
        )
    )


    if not workshop:

        return jsonify({
            'message': 'Workshop not found'
        }), 404


    # =================================================
    # Get registrations + user information
    # =================================================

    registrations = (
        workshop_registration_service
        .list_by_workshop(
            workshop_id
        )
    )


    # =================================================
    # Return directly
    # =================================================

    return jsonify(
        registrations
    ), 200