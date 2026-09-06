
from marshmallow import Schema, fields, validate


PAYMENT_STATUSES = [
    'Đang chờ xử lý',
    'Thành công',
    'Thất bại',
    'Đã hoàn tiền'
]


class PaymentRequestSchema(Schema):
    """
    Schema dùng khi TẠO payment mới.
    """

    invoice_id = fields.Int(required=True)

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

    status = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.OneOf(PAYMENT_STATUSES)
    )


class PaymentUpdateSchema(Schema):
    """
    Schema dùng khi provider XÁC NHẬN payment.

    PUT /payments/{pay_id}
    chỉ cần gửi status.
    """

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
