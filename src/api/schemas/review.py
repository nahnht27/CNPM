from marshmallow import Schema, fields

class ReviewRequestSchema(Schema):
    photographer_id = fields.Int(required=True)
    booking_id = fields.Int(required=True)
    rating = fields.Int(required=True)

class ReviewResponseSchema(Schema):
    id = fields.Int()
    photographer_id = fields.Int()
    booking_id = fields.Int()
    target_type = fields.Str()
    target_id = fields.Int()
    rating = fields.Int()
    comment = fields.Str()
    created_at = fields.Raw()
