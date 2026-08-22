from marshmallow import Schema, fields

class CategoryRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    category_type = fields.Str()

class CategoryResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    category_type = fields.Str()
    created_at = fields.Raw()
