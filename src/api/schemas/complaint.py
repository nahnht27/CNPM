from marshmallow import Schema, fields

class ComplaintRequestSchema(Schema):
    user_id = fields.Int(required=True)
    description = fields.Str(required=True)

class ComplaintResponseSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    booking_id = fields.Int()
    target_type = fields.Str()
    target_id = fields.Int()
    description = fields.Str()
    status = fields.Str()
    resolved_at = fields.Raw()
