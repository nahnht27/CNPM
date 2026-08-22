from marshmallow import Schema, fields


class EquipmentMaintenanceLogRequestSchema(Schema):
    equipment_id = fields.Int(required=True)
    maintenance_date = fields.Raw(required=True)
    status = fields.Str(required=True)


class EquipmentMaintenanceLogResponseSchema(Schema):
    id = fields.Int()
    equipment_id = fields.Int()
    maintenance_date = fields.Raw()
    description = fields.Str()
    cost = fields.Raw()
    performed_by = fields.Str()
    next_scheduled_date = fields.Raw()
    status = fields.Str()
