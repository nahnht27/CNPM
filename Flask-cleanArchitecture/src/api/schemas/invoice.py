from marshmallow import Schema, fields

class InvoiceRequestSchema(Schema):
    session_id = fields.Int(required=True)
    invoice_number = fields.Str(required=True)
    subtotal = fields.Raw(required=True)

class InvoiceResponseSchema(Schema):
    id = fields.Int()
    session_id = fields.Int()
    invoice_number = fields.Str()
    subtotal = fields.Raw()
    discount_amount = fields.Raw()
    tax_amount = fields.Raw()
    total_amount = fields.Raw()
    issued_at = fields.Raw()
