from marshmallow import Schema, fields


class SpaceAmenityRequestSchema(Schema):
    space_id = fields.Int(required=True)
    amenity_id = fields.Int(required=True)


class SpaceAmenityResponseSchema(Schema):
    id = fields.Int()
    space_id = fields.Int()
    amenity_id = fields.Int()
