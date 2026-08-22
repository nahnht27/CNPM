from marshmallow import Schema, fields

class ServicePackageRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    name = fields.Str(required=True)
    price = fields.Raw(required=True)

class ServicePackageResponseSchema(Schema):
    id = fields.Int()
    provider_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    price = fields.Raw()
    status = fields.Str()
    created_at = fields.Raw()
