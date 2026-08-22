from marshmallow import Schema, fields


class PostCommentRequestSchema(Schema):
    post_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)


class PostCommentResponseSchema(Schema):
    id = fields.Int()
    post_id = fields.Int()
    user_id = fields.Int()
    content = fields.Str()
    created_at = fields.Raw()
