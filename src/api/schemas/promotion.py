from marshmallow import Schema, fields

class PromotionRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    code = fields.Str(required=True)
    discount_value = fields.Raw(required=True)

class PromotionResponseSchema(Schema):
    id = fields.Int()
    provider_id = fields.Int()
    package_id = fields.Int()
    code = fields.Str()
    discount_type = fields.Str()
    discount_value = fields.Raw()
    start_date = fields.Raw()
    end_date = fields.Raw()
    usage_limit = fields.Int()
    status = fields.Str()
