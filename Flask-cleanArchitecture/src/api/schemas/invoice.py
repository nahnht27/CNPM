from marshmallow import Schema, fields

# 1. Schema cho từng mục chi tiết trong hóa đơn
class InvoiceItemDetailSchema(Schema):
    name = fields.Str()
    quantity = fields.Int()
    amount = fields.Raw()

class InvoiceRequestSchema(Schema):
    session_id = fields.Int(required=True)
    invoice_number = fields.Str(required=True)
    subtotal = fields.Raw(required=True)

class InvoiceResponseSchema(Schema):
    id = fields.Int()
    session_id = fields.Int()
    booking_id = fields.Int(allow_none=True)
    invoice_number = fields.Str()
    subtotal = fields.Raw()
    discount_amount = fields.Raw()
    tax_amount = fields.Raw()
    total_amount = fields.Raw()
    issued_at = fields.Raw()
    status = fields.Str(allow_none=True)
    
    # 2. Bổ sung trường invoice_details chứa danh sách item chi tiết
    invoice_details = fields.List(fields.Nested(InvoiceItemDetailSchema), dump_default=[])