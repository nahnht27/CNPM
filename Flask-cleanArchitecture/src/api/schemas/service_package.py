from marshmallow import Schema, fields, EXCLUDE


class ServicePackageRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    provider_id = fields.Int(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False, load_default="active")
    space_id = fields.Int(required=False, allow_none=True)


class ServicePackageResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    provider_id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price = fields.Float()
    status = fields.Str()
    created_at = fields.Str(allow_none=True)
    space_id = fields.Int(allow_none=True)
