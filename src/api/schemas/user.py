from marshmallow import Schema, fields


class UserRequestSchema(Schema):
	username = fields.Str(required=True)
	password = fields.Str(required=True)
	full_name = fields.Str()
	email = fields.Email()


class UserResponseSchema(Schema):
	id = fields.Int()
	username = fields.Str()
	full_name = fields.Str()
	email = fields.Str()
	phone = fields.Str()
	avatar = fields.Str()
	gender = fields.Str()
	created_at = fields.Raw()
	status = fields.Str()
	role_id = fields.Int()
