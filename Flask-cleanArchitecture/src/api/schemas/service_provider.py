from marshmallow import Schema, fields

class ServiceProviderRequestSchema(Schema):
    user_id = fields.Int(required=True)
    business_name = fields.Str(required=True)

class ServiceProviderResponseSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    business_name = fields.Str()
    tax_code = fields.Str()
    business_address = fields.Str()
    license_url = fields.Str()
    verification_status = fields.Str()
    approved_at = fields.Raw()
    bank_info = fields.Str()
    created_at = fields.Raw()
