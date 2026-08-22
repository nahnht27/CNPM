from marshmallow import Schema, fields

class PaymentRequestSchema(Schema):
    invoice_id = fields.Int(required=True)
    payment_method = fields.Str(required=True)
    amount = fields.Raw(required=True)

class PaymentResponseSchema(Schema):
    id = fields.Int()
    invoice_id = fields.Int()
    payment_method = fields.Str()
    amount = fields.Raw()
    status = fields.Str()
    paid_at = fields.Raw()
