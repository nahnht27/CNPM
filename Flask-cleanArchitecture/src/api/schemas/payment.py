from marshmallow import Schema, fields, validate


class PaymentRequestSchema(Schema):

    invoice_id = fields.Int(
        required=True
    )

    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf([
            'Chuyển khoản QR (VietQR)'
        ])
    )

    amount = fields.Raw(
        required=True
    )


class PaymentResponseSchema(Schema):

    id = fields.Int()

    invoice_id = fields.Int()

    payment_method = fields.Str()

    amount = fields.Raw()

    status = fields.Str()

    paid_at = fields.Raw()