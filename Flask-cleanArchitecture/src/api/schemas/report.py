from marshmallow import Schema, fields


class RevenueReportRequestSchema(Schema):
    from_date = fields.DateTime(required=True)
    to_date = fields.DateTime(required=True)


class RevenueReportResponseSchema(Schema):
    from_date = fields.DateTime()
    to_date = fields.DateTime()
    provider_id = fields.Integer(allow_none=True)
    total_revenue = fields.Float()
    total_bookings = fields.Integer()
    total_invoices = fields.Integer()
    revenue_by_month = fields.Dict(keys=fields.String(), values=fields.Float())