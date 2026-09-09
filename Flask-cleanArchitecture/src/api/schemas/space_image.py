from marshmallow import Schema, fields


class SpaceImageRequestSchema(Schema):
    space_id = fields.Int(required=True)
    image_url = fields.Str(required=True)


class SpaceImageResponseSchema(Schema):
    id = fields.Int()
    space_id = fields.Int()
    image_url = fields.Str()
    uploaded_at = fields.Raw()
