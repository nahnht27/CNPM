from marshmallow import Schema, fields


class PackageDetailRequestSchema(Schema):
    package_id = fields.Int(required=True)
    item_type = fields.Str(required=True)
    reference_id = fields.Int(required=True)
    quantity = fields.Raw(required=True)


class PackageDetailResponseSchema(Schema):
    id = fields.Int()
    package_id = fields.Int()
    item_type = fields.Str()
    reference_id = fields.Int()
    quantity = fields.Raw()
