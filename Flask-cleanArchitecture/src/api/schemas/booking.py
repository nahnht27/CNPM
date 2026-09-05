from marshmallow import Schema, fields

class BookingRequestSchema(Schema):
    photographer_id = fields.Int(required=True)
    space_id = fields.Int(required=True)
    package_id = fields.Int(required=False, allow_none=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    total_price = fields.Float(required=False, load_default=0.0)
    status = fields.Str(required=False)  # <-- Cần thiết để cập nhật trạng thái (pending/cancelled/checked_in/v.v.)

class BookingResponseSchema(Schema):
    id = fields.Int()
    photographer_id = fields.Int()
    space_id = fields.Int()
    package_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.Str()
    total_price = fields.Float()
    created_at = fields.DateTime()