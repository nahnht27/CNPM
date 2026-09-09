from marshmallow import Schema, fields


class ServiceProviderRequestSchema(Schema):

    user_id = fields.Int(
        required=False,
        allow_none=True
    )

    business_name = fields.Str(
        required=False,
        allow_none=True
    )

    tax_code = fields.Str(
        required=False,
        allow_none=True
    )

    business_address = fields.Str(
        required=False,
        allow_none=True
    )

    # URL hình/file giấy phép kinh doanh
    license_url = fields.Str(
        required=False,
        allow_none=True
    )

    verification_status = fields.Str(
        required=False,
        allow_none=True
    )

    approved_at = fields.Raw(
        required=False,
        allow_none=True
    )

    # Thông tin ngân hàng
    bank_info = fields.Str(
        required=False,
        allow_none=True
    )

    # URL hình QR thanh toán
    qr_code_url = fields.Str(
        required=False,
        allow_none=True
    )

    created_at = fields.Raw(
        required=False,
        allow_none=True
    )


class ServiceProviderResponseSchema(Schema):
    """
    Schema response tương ứng với ServiceProviderModel.
    """

    id = fields.Int()

    user_id = fields.Int()

    business_name = fields.Str()

    tax_code = fields.Str(
        allow_none=True
    )

    business_address = fields.Str()

    # URL hình/file giấy phép kinh doanh
    license_url = fields.Str(
        allow_none=True
    )

    verification_status = fields.Str()

    approved_at = fields.Raw(
        allow_none=True
    )

    # Thông tin ngân hàng
    bank_info = fields.Str(
        allow_none=True
    )

    # URL hình QR thanh toán
    qr_code_url = fields.Str(
        allow_none=True
    )

    created_at = fields.Raw(
        allow_none=True
    )