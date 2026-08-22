from marshmallow import Schema, fields


class BookingEquipmentRequestSchema(Schema):
    booking_id = fields.Int(required=True)
    equipment_id = fields.Int(required=True)
    quantity = fields.Int()
    rental_price = fields.Raw(required=True)


class BookingEquipmentResponseSchema(Schema):
    id = fields.Int()
    booking_id = fields.Int()
    equipment_id = fields.Int()
    quantity = fields.Int()
    rental_price = fields.Raw()
