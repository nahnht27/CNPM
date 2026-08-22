from marshmallow import Schema, fields

class RoleRequestSchema(Schema):
    name = fields.Str(required=True)

class RoleResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    created_at = fields.Raw()
    created_by = fields.Int()
    updated_at = fields.Raw()
    updated_by = fields.Int()
