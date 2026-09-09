from marshmallow import Schema, fields


class SessionConsumableUsageRequestSchema(Schema):
    session_id = fields.Int(required=True)
    consumable_id = fields.Int(required=True)
    quantity_used = fields.Raw(required=True)
    cost = fields.Raw(required=True)


class SessionConsumableUsageResponseSchema(Schema):
    id = fields.Int()
    session_id = fields.Int()
    consumable_id = fields.Int()
    quantity_used = fields.Raw()
    cost = fields.Raw()
