from marshmallow import Schema, fields


class InvoiceDetailRequestSchema(Schema):
    invoice_id = fields.Int(required=True)
    description = fields.Str(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Raw(required=True)


class InvoiceDetailResponseSchema(Schema):
    id = fields.Int()
    invoice_id = fields.Int()
    description = fields.Str()
    quantity = fields.Int()
    unit_price = fields.Raw()
    line_total = fields.Raw()
