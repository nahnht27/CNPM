from marshmallow import Schema, fields


# =========================================================
# CREATIVE SPACE REQUEST
# =========================================================

class CreativeSpaceRequestSchema(Schema):

    provider_id = fields.Int(
        required=True
    )

    name = fields.Str(
        required=True
    )

    category_id = fields.Int(
        required=True
    )

    description = fields.Str(
        allow_none=True,
        load_default=None
    )

    size_sqm = fields.Decimal(
        allow_none=True,
        load_default=None,
        as_string=True
    )

    max_capacity = fields.Int(
        required=True
    )

    operating_hours = fields.Str(
        required=True
    )

    pricing_model = fields.Str(
        required=True
    )

    base_price = fields.Decimal(
        required=True,
        as_string=True
    )

    status = fields.Str(
        required=True
    )

    address = fields.Str(
        required=True
    )


# =========================================================
# CREATIVE SPACE RESPONSE
# =========================================================

class CreativeSpaceResponseSchema(Schema):

    id = fields.Int()

    provider_id = fields.Int()

    name = fields.Str()

    category_id = fields.Int()

    category_name = fields.Str(
        allow_none=True
    )

    description = fields.Str(
        allow_none=True
    )

    size_sqm = fields.Decimal(
        allow_none=True,
        as_string=True
    )

    max_capacity = fields.Int()

    operating_hours = fields.Str()

    pricing_model = fields.Str()

    base_price = fields.Decimal(
        allow_none=True,
        as_string=True
    )

    status = fields.Str()

    address = fields.Str()

    image_url = fields.Str(
        allow_none=True
    )

    created_at = fields.DateTime(
        allow_none=True
    )

    images = fields.List(
        fields.Str()
    )