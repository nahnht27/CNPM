from marshmallow import Schema, fields

class PostRequestSchema(Schema):
    author_id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)

class PostResponseSchema(Schema):
    id = fields.Int()
    author_id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    category = fields.Str()
    status = fields.Str()
    created_at = fields.Raw()
