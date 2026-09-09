from marshmallow import Schema, fields, validate

# Danh sách trạng thái chuẩn của hệ thống Payment
PAYMENT_STATUSES = [
    'Đang chờ xử lý',
    'Thành công',
    'Thất bại',
    'Đã hoàn tiền'
]

# Các phương thức thanh toán được hỗ trợ
PAYMENT_METHODS = [
    'Chuyển khoản QR (VietQR)',
    'Tiền mặt',
    'Thẻ tín dụng'
]


class PaymentRequestSchema(Schema):
    """Schema dùng khi Photographer tạo yêu cầu thanh toán mới."""

    invoice_id = fields.Int(required=False, load_default=0)
    session_id = fields.Int(required=False, allow_none=True)

    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(PAYMENT_METHODS)
    )

    amount = fields.Decimal(
        required=True,
        as_string=False
    )

    discount_amount = fields.Decimal(required=False, load_default=0.0)
    tax_amount = fields.Decimal(required=False, load_default=0.0)

    # BẮT BUỘC: Đặt load_default là 'Đang chờ xử lý'
    # Nếu Frontend không gửi status, Marshmallow sẽ tự gán 'Đang chờ xử lý'
    status = fields.Str(
        required=False,
        allow_none=True,
        load_default='Đang chờ xử lý',
        validate=validate.OneOf(PAYMENT_STATUSES)
    )


class PaymentUpdateSchema(Schema):
    """Schema dùng khi Provider bấm cập nhật/xác nhận trạng thái."""

    status = fields.Str(
        required=True,
        validate=validate.OneOf(PAYMENT_STATUSES)
    )


class PaymentResponseSchema(Schema):
    """Schema serialize dữ liệu trả về cho Frontend."""

    id = fields.Int()
    invoice_id = fields.Int()
    payment_method = fields.Str()
    amount = fields.Decimal(as_string=True)
    status = fields.Str()
    created_at = fields.DateTime(allow_none=True)
    paid_at = fields.DateTime(allow_none=True)