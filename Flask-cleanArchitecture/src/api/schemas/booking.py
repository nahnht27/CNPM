from marshmallow import Schema, fields


class BookingRequestSchema(Schema):
    photographer_id = fields.Int(required=True)
    space_id = fields.Int(required=True)
    package_id = fields.Int(required=False, allow_none=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    total_price = fields.Float(required=False, load_default=0.0)
    status = fields.Str(required=False)


class BookingUpdateSchema(Schema):
    photographer_id = fields.Int(required=False)
    space_id = fields.Int(required=False)
    package_id = fields.Int(required=False, allow_none=True)
    start_time = fields.DateTime(required=False)
    end_time = fields.DateTime(required=False)
    total_price = fields.Float(required=False)
    status = fields.Str(required=False)


class ProviderBookingResponseSchema(Schema):
    id = fields.Int()
    photographer_id = fields.Int()
    space_id = fields.Int()
    package_id = fields.Int(allow_none=True)

    start_time = fields.DateTime()
    end_time = fields.DateTime()

    status = fields.Str()
    total_price = fields.Float()
    created_at = fields.DateTime()

    # Invoice của Booking
    invoice_id = fields.Int(allow_none=True)

    provider_id = fields.Int()
    space_name = fields.Str(allow_none=True)


class BookingResponseSchema(Schema):
    id = fields.Int()
    photographer_id = fields.Int()
    space_id = fields.Int()
    package_id = fields.Int(allow_none=True)

    start_time = fields.DateTime()
    end_time = fields.DateTime()

    status = fields.Str()
    total_price = fields.Float()
    created_at = fields.DateTime()

    # Invoice của Booking
    invoice_id = fields.Int(allow_none=True)