from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

from api.schemas.auth import (
    RigisterUserRequestSchema,
    RigisterUserResponseSchema
)

from services.auth_service import AuthService
from infrastructure.repositories.auth_repository import AuthRepository

import jwt
from werkzeug.security import generate_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_service = AuthService(AuthRepository())

register_request = RigisterUserRequestSchema()
register_response = RigisterUserResponseSchema()


@auth_bp.route('/check_router', methods=['GET'])
def check_router():
    """
    Check router
    ---
    get:
      summary: Check router health
      tags:
        - Auth
      responses:
        200:
          description: Router is working
    """
    return jsonify({
        'message': 'Router is working!'
    }), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    ---
    post:
      summary: Login user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginUserRequest'
      tags:
        - Auth
      responses:
        200:
          description: Successful login
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginUserResponse'
        401:
          description: Invalid credentials
    """

    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'Dữ liệu đăng nhập không hợp lệ.'
        }), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'error': 'Vui lòng nhập tên đăng nhập và mật khẩu.'
        }), 400

    user = auth_service.login(username, password)

    if not user:
        return jsonify({
            'error': 'Thông tin đăng nhập không chính xác.'
        }), 401

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({
        'token': token,
        'username': user.username,
        'user_id': user.id,
        'role_id': user.role_id
    }), 200


@auth_bp.route('/signup', methods=['POST'])
def register():
    """
    Register a new user
    ---
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RigisterUserRequest'
      tags:
        - Auth
      responses:
        201:
          description: User registered successfully
        400:
          description: Invalid input or user exists
        500:
          description: Registration failed
    """

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Dữ liệu đăng ký không hợp lệ.'
        }), 400

    # =========================
    # VALIDATE SCHEMA
    # =========================

    errors = register_request.validate(data)

    if errors:
        return jsonify(errors), 400

    # =========================
    # GET DATA
    # =========================

    username = data.get('username')
    password = data.get('password')
    passwordconfirm = data.get('passwordconfirm')
    email = data.get('email')
    role_id = data.get('role_id')

    # =========================
    # VALIDATE REQUIRED FIELDS
    # =========================

    if not username or not password or not passwordconfirm or not email:
        return jsonify({
            'message': (
                'Missing required fields: '
                'username, password, passwordconfirm, email'
            )
        }), 400

    # =========================
    # CONVERT ROLE ID
    # =========================
    # Frontend select trả về string "2" hoặc "3"
    # Backend chuyển thành integer 2 hoặc 3

    try:
        role_id = int(role_id)
    except (TypeError, ValueError):
        return jsonify({
            'message': 'Invalid role_id'
        }), 400

    # =========================
    # CHECK ROLE
    # =========================
    #
    # RoleID:
    # 1 = Admin
    # 2 = Photographer
    # 3 = Service Provider
    #
    # Người dùng chỉ được đăng ký:
    # 2 = Photographer
    # 3 = Service Provider

    if role_id not in [2, 3]:
        return jsonify({
            'message': 'Invalid role_id'
        }), 400

    # =========================
    # CHECK PASSWORD
    # =========================

    if password != passwordconfirm:
        return jsonify({
            'message': 'Passwords do not match'
        }), 400

    # =========================
    # CHECK EXIST USER
    # =========================

    if auth_service.check_exist(username):
        return jsonify({
            'message': 'User already exists. Please login.'
        }), 400

    # =========================
    # HASH PASSWORD
    # =========================

    password_hashed = generate_password_hash(password)

    # =========================
    # REGISTER USER
    # =========================

    new_user = auth_service.register(
        username,
        password_hashed,
        email,
        role_id
    )

    # =========================
    # CHECK REGISTER RESULT
    # =========================

    if not new_user:
        return jsonify({
            'message': 'Registration failed'
        }), 500

    # =========================
    # RESPONSE
    # =========================

    result = register_response.dump(new_user)

    return jsonify(result), 201