from marshmallow import Schema, fields, validate

PAYMENT_STATUSES = [
    'Đang chờ xử lý',
    'Thành công',
    'Thất bại',
    'Đã hoàn tiền'
]


class PaymentRequestSchema(Schema):
    """Schema dùng khi TẠO payment mới."""

    # Cho phép invoice_id = 0 hoặc không bắt buộc truyền
    invoice_id = fields.Int(required=False, load_default=0)

    # Khai báo session_id để Marshmallow giữ lại trường này khi load()
    session_id = fields.Int(required=False, allow_none=True)

    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf([
            'Chuyển khoản QR (VietQR)'
        ])
    )

    amount = fields.Decimal(
        required=True,
        as_string=False
    )

    # Khai báo thêm để không bị lọc mất
    discount_amount = fields.Decimal(required=False, load_default=0.0)
    tax_amount = fields.Decimal(required=False, load_default=0.0)

    status = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.OneOf(PAYMENT_STATUSES)
    )


class PaymentUpdateSchema(Schema):
    status = fields.Str(
        required=True,
        validate=validate.OneOf(PAYMENT_STATUSES)
    )


class PaymentResponseSchema(Schema):
    id = fields.Int()
    invoice_id = fields.Int()
    payment_method = fields.Str()
    amount = fields.Decimal(as_string=True)
    status = fields.Str()
    paid_at = fields.DateTime(allow_none=True)