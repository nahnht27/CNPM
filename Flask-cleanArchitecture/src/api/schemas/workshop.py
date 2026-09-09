from marshmallow import Schema, fields


class WorkshopRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    location = fields.Str(required=True)
    start_time = fields.Raw(required=True)
    end_time = fields.Raw(required=True)
    capacity = fields.Int(required=True)
    status = fields.Str(required=True)


class WorkshopResponseSchema(Schema):
    id = fields.Int()
    provider_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    location = fields.Str()
    start_time = fields.Raw()
    end_time = fields.Raw()
    capacity = fields.Int()
    fee = fields.Raw()
    status = fields.Str()
    created_at = fields.Raw()