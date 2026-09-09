import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from supabase import create_client
from services.service_provider_service import ServiceProviderService
from infrastructure.repositories.service_provider_repository import (ServiceProviderRepository)
from api.schemas.service_provider import (ServiceProviderRequestSchema,ServiceProviderResponseSchema)
from infrastructure.databases.postgres import session


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

SUPABASE_BUCKET = os.getenv(
    "SUPABASE_STORAGE_BUCKET",
    "provider-documents"
)


if not SUPABASE_URL:
    raise RuntimeError(
        "SUPABASE_URL chưa được cấu hình trong file .env"
    )


if not SUPABASE_SERVICE_KEY:
    raise RuntimeError(
        "SUPABASE_SERVICE_KEY chưa được cấu hình trong file .env"
    )


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)


# =========================================================
# FILE CONFIGURATION
# =========================================================

ALLOWED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}

ALLOWED_LICENSE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf"
}

MAX_FILE_SIZE = 10 * 1024 * 1024

bp = Blueprint(
    "service_provider",
    __name__,
    url_prefix="/service-providers"
)


# =========================================================
# SERVICE
# =========================================================

service_provider_service = ServiceProviderService(
    ServiceProviderRepository(session)
)


# =========================================================
# SCHEMA
# =========================================================

request_schema = ServiceProviderRequestSchema()
response_schema = ServiceProviderResponseSchema()


# =========================================================
# HELPER - REQUEST DATA
# =========================================================

def get_request_data():
    """
    Đọc dữ liệu từ:

    1. application/json
    2. multipart/form-data

    Với FormData:
        request.form  -> field text
        request.files -> file
    """

    if (
        request.content_type
        and request.content_type.startswith(
            "multipart/form-data"
        )
    ):
        return request.form.to_dict()

    data = request.get_json(
        silent=True
    )

    if data is None:
        return {}

    return data


# =========================================================
# HELPER - UPLOAD SUPABASE
# =========================================================

def upload_provider_file(
    file,
    provider_id,
    file_type
):
    """
    Upload file của Service Provider
    lên Supabase Storage.

    file_type:
        qr
        license

    Return:

        {
            "path": "...",
            "url": "..."
        }
    """

    if not file:
        return None

    # -----------------------------------------------------
    # Kiểm tra filename
    # -----------------------------------------------------

    if not file.filename:
        raise ValueError(
            "File được gửi lên nhưng không có tên file."
        )

    filename = secure_filename(
        file.filename
    )

    if not filename:
        raise ValueError(
            "Tên file không hợp lệ."
        )

    # -----------------------------------------------------
    # Extension
    # -----------------------------------------------------

    extension = os.path.splitext(
        filename
    )[1].lower()

    # -----------------------------------------------------
    # Kiểm tra loại file
    # -----------------------------------------------------

    if file_type == "qr":

        if extension not in ALLOWED_IMAGE_EXTENSIONS:

            raise ValueError(
                "QR Code chỉ chấp nhận "
                "PNG, JPG, JPEG hoặc WEBP."
            )

        allowed_mime_types = {
            "image/png",
            "image/jpeg",
            "image/webp"
        }

    elif file_type == "license":

        if extension not in ALLOWED_LICENSE_EXTENSIONS:

            raise ValueError(
                "Giấy phép chỉ chấp nhận "
                "PNG, JPG, JPEG, WEBP hoặc PDF."
            )

        allowed_mime_types = {
            "image/png",
            "image/jpeg",
            "image/webp",
            "application/pdf"
        }

    else:

        raise ValueError(
            "Loại file upload không hợp lệ."
        )

    # -----------------------------------------------------
    # MIME type
    # -----------------------------------------------------

    mime_type = (
        file.mimetype
        or "application/octet-stream"
    )

    if mime_type not in allowed_mime_types:

        raise ValueError(
            f"Loại file '{mime_type}' không được hỗ trợ."
        )

    # -----------------------------------------------------
    # Đọc file
    # -----------------------------------------------------

    file_bytes = file.read()

    if not file_bytes:

        raise ValueError(
            "File rỗng, không thể upload."
        )

    # -----------------------------------------------------
    # Kiểm tra kích thước
    # -----------------------------------------------------

    if len(file_bytes) > MAX_FILE_SIZE:

        raise ValueError(
            "File quá lớn. "
            "Kích thước tối đa là 10MB."
        )

    # -----------------------------------------------------
    # Tạo tên file unique
    # -----------------------------------------------------

    unique_filename = (
        f"{uuid.uuid4().hex}_{filename}"
    )

    # -----------------------------------------------------
    # Tạo path Storage
    # -----------------------------------------------------

    if file_type == "qr":

        storage_path = (
            f"providers/"
            f"{provider_id}/"
            f"qr-codes/"
            f"{unique_filename}"
        )

    else:

        storage_path = (
            f"providers/"
            f"{provider_id}/"
            f"licenses/"
            f"{unique_filename}"
        )

    # -----------------------------------------------------
    # Upload
    # -----------------------------------------------------

    try:

        supabase.storage \
            .from_(SUPABASE_BUCKET) \
            .upload(
                storage_path,
                file_bytes,
                file_options={
                    "content-type": mime_type,
                    "cache-control": "3600",
                    "upsert": "false"
                }
            )

    except Exception as e:

        print(
            "[Supabase Upload Error]",
            str(e)
        )

        raise RuntimeError(
            "Không thể upload file lên "
            f"Supabase Storage: {str(e)}"
        )

    # -----------------------------------------------------
    # Lấy public URL
    # -----------------------------------------------------

    try:

        public_url = (
            supabase.storage
            .from_(SUPABASE_BUCKET)
            .get_public_url(
                storage_path
            )
        )

    except Exception as e:

        print(
            "[Supabase URL Error]",
            str(e)
        )

        # Upload được nhưng lấy URL thất bại
        # → cố gắng xóa file vừa upload

        try:

            supabase.storage \
                .from_(SUPABASE_BUCKET) \
                .remove([
                    storage_path
                ])

        except Exception:
            pass

        raise RuntimeError(
            "Upload thành công nhưng "
            "không thể lấy URL file."
        )

    return {
        "path": storage_path,
        "url": public_url
    }


# =========================================================
# HELPER - DELETE SUPABASE FILE
# =========================================================

def delete_storage_file(
    storage_path
):
    """
    Xóa file vừa upload nếu
    database update thất bại.
    """

    if not storage_path:
        return

    try:

        supabase.storage \
            .from_(SUPABASE_BUCKET) \
            .remove([
                storage_path
            ])

        print(
            "[Supabase] Deleted:",
            storage_path
        )

    except Exception as e:

        print(
            "[Supabase Delete Error]:",
            str(e)
        )


# =========================================================
# GET ALL
# =========================================================

@bp.route(
    "/",
    methods=["GET"]
)
def list_providers():

    try:

        providers = (
            service_provider_service
            .list_providers()
        )

        return jsonify(
            response_schema.dump(
                providers,
                many=True
            )
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            "message":
                "Không thể tải danh sách "
                "nhà cung cấp dịch vụ.",
            "error": str(e)
        }), 500


# =========================================================
# GET BY ID
# =========================================================

@bp.route(
    "/<int:provider_id>",
    methods=["GET"]
)
def get_provider(provider_id):

    try:

        provider = (
            service_provider_service
            .get_provider(
                provider_id
            )
        )

        if not provider:

            return jsonify({
                "message":
                    "Không tìm thấy "
                    "nhà cung cấp dịch vụ."
            }), 404

        return jsonify(
            response_schema.dump(
                provider
            )
        ), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            "message":
                "Không thể tải thông tin "
                "nhà cung cấp dịch vụ.",
            "error": str(e)
        }), 500


# =========================================================
# CREATE
# =========================================================

@bp.route(
    "/",
    methods=["POST"]
)
def create_provider():

    try:

        data = get_request_data()

        # -------------------------------------------------
        # user_id bắt buộc
        # -------------------------------------------------

        if not data.get("user_id"):

            return jsonify({
                "message":
                    "Dữ liệu không hợp lệ.",
                "errors": {
                    "user_id": [
                        "Trường user_id là bắt buộc "
                        "khi tạo nhà cung cấp."
                    ]
                }
            }), 400

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        errors = request_schema.validate(
            data
        )

        if errors:

            return jsonify({
                "message":
                    "Dữ liệu không hợp lệ.",
                "errors": errors
            }), 400

        # -------------------------------------------------
        # CREATE
        # -------------------------------------------------

        provider = (
            service_provider_service
            .create_provider(
                **data
            )
        )

        return jsonify(
            response_schema.dump(
                provider
            )
        ), 201

    except Exception as e:

        session.rollback()

        return jsonify({
            "message":
                "Không thể tạo "
                "nhà cung cấp dịch vụ.",
            "error": str(e)
        }), 500


# =========================================================
# UPDATE
# =========================================================

@bp.route(
    "/<int:provider_id>",
    methods=["PUT"]
)
def update_provider(provider_id):

    # -----------------------------------------------------
    # Lưu path các file mới upload
    #
    # Nếu database update thất bại,
    # các file này sẽ được xóa.
    # -----------------------------------------------------

    uploaded_paths = []

    try:

        # -------------------------------------------------
        # Kiểm tra provider
        # -------------------------------------------------

        provider = (
            service_provider_service
            .get_provider(
                provider_id
            )
        )

        if not provider:

            return jsonify({
                "message":
                    "Không tìm thấy "
                    "nhà cung cấp dịch vụ."
            }), 404

        # -------------------------------------------------
        # Request data
        # -------------------------------------------------

        data = get_request_data()

        print(
            "\n======================================"
        )

        print(
            "[ServiceProvider PUT]"
        )

        print(
            "Content-Type:",
            request.content_type
        )

        print(
            "Data:",
            data
        )

        # -------------------------------------------------
        # Files
        # -------------------------------------------------

        license_file = request.files.get(
            "license_file"
        )

        qr_code_file = request.files.get(
            "qr_code"
        )

        if license_file:

            print(
                "License:",
                license_file.filename
            )

        if qr_code_file:

            print(
                "QR:",
                qr_code_file.filename
            )

        # -------------------------------------------------
        # Không cho sửa user_id
        # -------------------------------------------------

        data.pop(
            "user_id",
            None
        )

        # -------------------------------------------------
        # Frontend field cũ
        # -------------------------------------------------

        unsupported_fields = [
            "bank_name",
            "account_number",
            "account_name",
            "qr_code"
        ]

        for field in unsupported_fields:

            data.pop(
                field,
                None
            )

        # -------------------------------------------------
        # URL cũ không được frontend tự truyền
        #
        # Backend sẽ tự tạo URL sau khi upload.
        # -------------------------------------------------

        data.pop(
            "license_url",
            None
        )

        data.pop(
            "qr_code_url",
            None
        )

        # -------------------------------------------------
        # Allowed text fields
        # -------------------------------------------------

        allowed_fields = {
            "business_name",
            "tax_code",
            "business_address",
            "verification_status",
            "approved_at",
            "bank_info"
        }

        data = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        # -------------------------------------------------
        # Upload LICENSE
        # -------------------------------------------------

        if license_file:

            license_result = (
                upload_provider_file(
                    license_file,
                    provider_id,
                    "license"
                )
            )

            data["license_url"] = (
                license_result["url"]
            )

            uploaded_paths.append(
                license_result["path"]
            )

            print(
                "License URL:",
                license_result["url"]
            )

        # -------------------------------------------------
        # Upload QR
        # -------------------------------------------------

        if qr_code_file:

            qr_result = (
                upload_provider_file(
                    qr_code_file,
                    provider_id,
                    "qr"
                )
            )

            data["qr_code_url"] = (
                qr_result["url"]
            )

            uploaded_paths.append(
                qr_result["path"]
            )

            print(
                "QR URL:",
                qr_result["url"]
            )

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        errors = request_schema.validate(
            data
        )

        if errors:

            print(
                "[ServiceProvider PUT] "
                "Validation errors:",
                errors
            )

            # Xóa file đã upload
            for path in uploaded_paths:
                delete_storage_file(path)

            return jsonify({
                "message":
                    "Dữ liệu không hợp lệ.",
                "errors": errors
            }), 400

        # -------------------------------------------------
        # Không có dữ liệu
        # -------------------------------------------------

        if not data:

            return jsonify({
                "message":
                    "Không có dữ liệu cần cập nhật."
            }), 400

        # -------------------------------------------------
        # UPDATE DATABASE
        # -------------------------------------------------

        updated_provider = (
            service_provider_service
            .update_provider(
                provider_id,
                **data
            )
        )

        # -------------------------------------------------
        # Thành công
        # -------------------------------------------------

        print(
            "[ServiceProvider PUT] "
            "Update successful."
        )

        print(
            "======================================\n"
        )

        return jsonify(
            response_schema.dump(
                updated_provider
            )
        ), 200

    except ValueError as e:

        session.rollback()

        # -------------------------------------------------
        # Rollback Supabase
        # -------------------------------------------------

        for path in uploaded_paths:

            delete_storage_file(
                path
            )

        print(
            "[ServiceProvider PUT] "
            "ValueError:",
            str(e)
        )

        return jsonify({
            "message": str(e)
        }), 400

    except Exception as e:

        session.rollback()

        # -------------------------------------------------
        # Rollback Supabase
        # -------------------------------------------------

        for path in uploaded_paths:

            delete_storage_file(
                path
            )

        print(
            "[ServiceProvider PUT] ERROR:",
            str(e)
        )

        return jsonify({
            "message":
                "Không thể cập nhật "
                "thông tin nhà cung cấp dịch vụ.",
            "error": str(e)
        }), 500

@bp.route(
    "/<int:provider_id>",
    methods=["DELETE"]
)
def delete_provider(provider_id):

    try:

        provider = (
            service_provider_service
            .get_provider(
                provider_id
            )
        )

        if not provider:

            return jsonify({
                "message":
                    "Không tìm thấy "
                    "nhà cung cấp dịch vụ."
            }), 404

        service_provider_service.delete_provider(
            provider_id
        )

        return "", 204

    except Exception as e:

        session.rollback()

        return jsonify({
            "message":
                "Không thể xóa "
                "nhà cung cấp dịch vụ.",
            "error": str(e)
        }), 500