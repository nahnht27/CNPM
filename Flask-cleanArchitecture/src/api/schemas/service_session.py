from marshmallow import Schema, fields


class ServiceSessionRequestSchema(Schema):
    booking_id = fields.Int(required=True)
    check_in_method = fields.Str(required=False, allow_none=True)
    notes = fields.Str(required=False, allow_none=True)


class ServiceSessionUpdateSchema(Schema):
    check_in_time = fields.DateTime(required=False, allow_none=True)
    check_out_time = fields.DateTime(required=False, allow_none=True)
    check_in_method = fields.Str(required=False, allow_none=True)
    actual_duration_minutes = fields.Int(required=False, allow_none=True)
    notes = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False)


class ServiceSessionResponseSchema(Schema):
    id = fields.Int()
    booking_id = fields.Int()

    check_in_time = fields.DateTime(allow_none=True)
    check_out_time = fields.DateTime(allow_none=True)

    check_in_method = fields.Str(allow_none=True)

    actual_duration_minutes = fields.Int(
        allow_none=True
    )

    notes = fields.Str(allow_none=True)

    status = fields.Str()

