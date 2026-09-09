from marshmallow import Schema, fields


class SessionEquipmentUsageRequestSchema(Schema):
    session_id = fields.Int(required=True)
    equipment_id = fields.Int(required=True)
    quantity = fields.Int(required=True)


class SessionEquipmentUsageResponseSchema(Schema):
    id = fields.Int()
    session_id = fields.Int()
    equipment_id = fields.Int()
    quantity = fields.Int()
    notes = fields.Str()
