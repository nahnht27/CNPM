import email
from unittest import result

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

import random
import time

from email_service import send_reset_otp
from werkzeug.security import generate_password_hash

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
reset_store = {}


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

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():

    data = request.get_json() or {}

    email = (
        data.get('email') or ''
    ).strip().lower()

    if not email:
        return jsonify({
            'message': 'Vui lòng nhập email.'
        }), 400

    user = auth_service.get_by_email(email)

    if not user:
        return jsonify({
            'message': 'Email không tồn tại.'
        }), 404

    otp = str(
        random.randint(100000, 999999)
    )

    reset_store[email] = {
        'otp': otp,
        'expires_at': time.time() + 300,
        'verified': False
    }

    if not send_reset_otp(email, otp):

        reset_store.pop(email, None)

        return jsonify({
            'message': (
                'Không thể gửi mã OTP. '
                'Hãy kiểm tra cấu hình email.'
            )
        }), 500

    return jsonify({
        'message':
            'Mã OTP đã được gửi đến email của bạn.'
    }), 200


@auth_bp.route('/verify-reset-code', methods=['POST'])
def verify_reset_code():

    data = request.get_json() or {}

    email = (
        data.get('email') or ''
    ).strip().lower()

    otp = str(
        data.get('otp') or ''
    ).strip()

    record = reset_store.get(email)

    if not record:
        return jsonify({
            'message': (
                'Phiên đặt lại mật khẩu '
                'không tồn tại. '
                'Vui lòng yêu cầu mã mới.'
            )
        }), 400

    if time.time() > record['expires_at']:

        reset_store.pop(email, None)

        return jsonify({
            'message': 'Mã OTP đã hết hạn.'
        }), 400

    if otp != record['otp']:

        return jsonify({
            'message': 'Mã OTP không chính xác.'
        }), 400

    record['verified'] = True

    return jsonify({
        'message':
            'Xác thực OTP thành công.'
    }), 200


@auth_bp.route('/resend-reset-code', methods=['POST'])
def resend_reset_code():

    data = request.get_json() or {}

    email = (
        data.get('email') or ''
    ).strip().lower()

    if not email:
        return jsonify({
            'message': 'Vui lòng nhập email.'
        }), 400

    user = auth_service.get_by_email(email)

    if not user:
        return jsonify({
            'message': 'Email không tồn tại.'
        }), 404

    otp = str(
        random.randint(100000, 999999)
    )

    reset_store[email] = {
        'otp': otp,
        'expires_at': time.time() + 300,
        'verified': False
    }

    if not send_reset_otp(email, otp):

        return jsonify({
            'message':
                'Không thể gửi lại mã OTP.'
        }), 500

    return jsonify({
        'message':
            'Mã OTP mới đã được gửi.'
    }), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():

    data = request.get_json() or {}

    email = (
        data.get('email') or ''
    ).strip().lower()

    password = (
        data.get('password') or ''
    )

    passwordconfirm = (
        data.get('passwordconfirm') or ''
    )

    record = reset_store.get(email)

    if not record or not record.get('verified'):

        return jsonify({
            'message':
                'Bạn chưa xác thực mã OTP.'
        }), 400

    if time.time() > record['expires_at']:

        reset_store.pop(email, None)

        return jsonify({
            'message':
                'Phiên đặt lại mật khẩu đã hết hạn.'
        }), 400

    if len(password) < 6:

        return jsonify({
            'message':
                'Mật khẩu phải có ít nhất 6 ký tự.'
        }), 400

    if password != passwordconfirm:

        return jsonify({
            'message':
                'Mật khẩu xác nhận không khớp.'
        }), 400

    user = auth_service.get_by_email(email)

    if not user:

        return jsonify({
            'message':
                'Email không tồn tại.'
        }), 404

    print("DEBUG 1 - USER:", user)
    print("DEBUG 2 - USER ID:", user.ID)
    password_hash = generate_password_hash(password)
    print("DEBUG 3 - HASH CREATED")
    result = auth_service.update_password(
    user.ID,
    password_hash
)
    print("DEBUG 4 - UPDATE RESULT:", result)
    if not result:
        return jsonify({
        'message': 'Không thể cập nhật mật khẩu.'
    }), 500
    reset_store.pop(email, None)
    return jsonify({
    'message': 'Đổi mật khẩu thành công.'
}), 200

    reset_store.pop(email, None)

    return jsonify({
        'message':
            'Đổi mật khẩu thành công.'
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