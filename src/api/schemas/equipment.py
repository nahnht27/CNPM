from marshmallow import Schema, fields

class EquipmentRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    name = fields.Str(required=True)

class EquipmentResponseSchema(Schema):
    id = fields.Int()
    provider_id = fields.Int()
    space_id = fields.Int()
    category_id = fields.Int()
    name = fields.Str()
    brand = fields.Str()
    condition = fields.Str()
    rental_price = fields.Raw()
    status = fields.Str()
    purchase_date = fields.Raw()
    created_at = fields.Raw()
