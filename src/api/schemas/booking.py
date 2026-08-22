from marshmallow import Schema, fields

class BookingRequestSchema(Schema):
    photographer_id = fields.Int(required=True)
    space_id = fields.Int(required=True)
    start_time = fields.Raw(required=True)
    end_time = fields.Raw(required=True)

class BookingResponseSchema(Schema):
    id = fields.Int()
    photographer_id = fields.Int()
    space_id = fields.Int()
    package_id = fields.Int()
    start_time = fields.Raw()
    end_time = fields.Raw()
    status = fields.Str()
    total_price = fields.Raw()
    created_at = fields.Raw()
