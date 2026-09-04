from marshmallow import Schema, fields, EXCLUDE

class ServicePackageRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Bỏ qua các trường thừa nếu client truyền lên

    provider_id = fields.Int(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=False, allow_none=True)


class ServicePackageResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # Không dùng attribute="..." nữa vì Model đã tự map tên cột thành id, provider_id, name...
    id = fields.Int()
    provider_id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price = fields.Float() # Ép kiểu Float an toàn cho JS
    status = fields.Str()
    created_at = fields.Str(allow_none=True)
    
    # Trường space_id để Frontend lọc theo từng Không gian
    space_id = fields.Int(dump_default=None, allow_none=True)