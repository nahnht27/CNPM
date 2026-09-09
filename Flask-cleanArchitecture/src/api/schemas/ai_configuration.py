from marshmallow import Schema, fields


class AIConfigurationRequestSchema(Schema):
    config_key = fields.Str(required=True)
    config_value = fields.Str(required=True)
    is_active = fields.Bool(required=True)


class AIConfigurationResponseSchema(Schema):
    id = fields.Int()
    config_key = fields.Str()
    config_value = fields.Str()
    is_active = fields.Bool()
    updated_at = fields.Raw()
    updated_by = fields.Int()
