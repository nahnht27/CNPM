from marshmallow import Schema, fields


class AIInteractionLogRequestSchema(Schema):
    user_id = fields.Int(required=True)
    interaction_type = fields.Str(required=True)
    query_text = fields.Str()


class AIInteractionLogResponseSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    interaction_type = fields.Str()
    query_text = fields.Str()
    response_text = fields.Str()
    created_at = fields.Raw()
