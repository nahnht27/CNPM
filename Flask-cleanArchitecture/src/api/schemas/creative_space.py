from marshmallow import Schema, fields


class CreativeSpaceRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    name = fields.Str(required=True)
    category_id = fields.Int(required=True)


class CreativeSpaceResponseSchema(Schema):
    id = fields.Int()
    provider_id = fields.Int()
    name = fields.Str()
    category_id = fields.Int()
    category_name = fields.Str(allow_none=True)

    description = fields.Str(allow_none=True)

    size_sqm = fields.Raw(allow_none=True)
    max_capacity = fields.Int()
    operating_hours = fields.Str()
    pricing_model = fields.Str()
    base_price = fields.Raw()

    status = fields.Str()
    address = fields.Str()

    created_at = fields.Raw()

    images = fields.List(
        fields.Str(),
        allow_none=True
    )