from marshmallow import Schema, fields


class ServiceSessionRequestSchema(Schema):
    booking_id = fields.Int(required=True)


class ServiceSessionResponseSchema(Schema):
    id = fields.Int()
    booking_id = fields.Int()
    check_in_time = fields.Raw()
    check_out_time = fields.Raw()
    check_in_method = fields.Str()
    actual_duration_minutes = fields.Int()
    notes = fields.Str()
    status = fields.Str()
