from marshmallow import Schema, fields


class ConsumableRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    name = fields.Str(required=True)
    consumable_type = fields.Str(required=True)
    unit = fields.Str(required=True)
    unit_price = fields.Raw(required=True)


class ConsumableResponseSchema(Schema):
    id = fields.Int()
    provider_id = fields.Int()
    name = fields.Str()
    consumable_type = fields.Str()
    unit = fields.Str()
    stock_quantity = fields.Raw()
    unit_price = fields.Raw()
    expiry_date = fields.Raw()
