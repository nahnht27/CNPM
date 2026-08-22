from marshmallow import Schema, fields

class NotificationRequestSchema(Schema):
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)

class NotificationResponseSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    type = fields.Str()
    is_read = fields.Bool()
    created_at = fields.Raw()
