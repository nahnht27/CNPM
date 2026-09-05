from marshmallow import Schema, fields, EXCLUDE


class EquipmentRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    provider_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    name = fields.Str(required=True)
    space_id = fields.Int(required=False, allow_none=True)
    brand = fields.Str(required=False, allow_none=True)
    condition = fields.Str(required=False, allow_none=True)
    rental_price = fields.Float(required=False, allow_none=True)
    status = fields.Str(required=False, load_default="available")
    purchase_date = fields.Str(required=False, allow_none=True)


class EquipmentResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # Không dùng attribute="..." nữa — Model đã map cột DB sang
    # Python attribute snake_case (id, name, rental_price...) sẵn rồi
    id = fields.Int()
    provider_id = fields.Int()
    space_id = fields.Int(allow_none=True)
    category_id = fields.Int()
    name = fields.Str()
    brand = fields.Str(allow_none=True)
    condition = fields.Str(allow_none=True)
    rental_price = fields.Float()
    status = fields.Str()
    purchase_date = fields.Str(allow_none=True)
    created_at = fields.Str(allow_none=True)