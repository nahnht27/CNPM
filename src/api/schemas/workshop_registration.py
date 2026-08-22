from marshmallow import Schema, fields


class WorkshopRegistrationRequestSchema(Schema):
    workshop_id = fields.Int(required=True)
    user_id = fields.Int(required=True)


class WorkshopRegistrationResponseSchema(Schema):
    id = fields.Int()
    workshop_id = fields.Int()
    user_id = fields.Int()
    registered_at = fields.Raw()
    status = fields.Str()
