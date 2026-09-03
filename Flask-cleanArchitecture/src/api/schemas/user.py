from marshmallow import Schema, fields


class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    full_name = fields.Str()
    email = fields.Email()
    phone = fields.Str(allow_none=True)
    avatar = fields.Str(allow_none=True)
    gender = fields.Str(allow_none=True)
    created_at = fields.Raw()
    status = fields.Str()
    role_id = fields.Int()


class UserUpdateRequestSchema(Schema):
    full_name = fields.Str(required=False)
    email = fields.Email(required=False)
    phone = fields.Str(required=False, allow_none=True)
    avatar = fields.Str(required=False, allow_none=True)
    gender = fields.Str(required=False, allow_none=True)