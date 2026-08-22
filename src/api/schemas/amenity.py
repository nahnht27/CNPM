from marshmallow import Schema, fields


class AmenityRequestSchema(Schema):
    name = fields.Str(required=True)


class AmenityResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
