from marshmallow import Schema, fields

# 1. Class Request Schema mà Swagger đang gọi tìm nhưng bị thiếu
class EquipmentRequestSchema(Schema):
    provider_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    name = fields.Str(required=True)
    space_id = fields.Int(required=False, allow_none=True)
    brand = fields.Str(required=False)
    condition = fields.Str(required=False)
    rental_price = fields.Float(required=False)

# 2. Class Response Schema đã sửa chuẩn tên thuộc tính DB
class EquipmentResponseSchema(Schema):
    id = fields.Int(attribute="EquipmentID")
    provider_id = fields.Int(attribute="ProviderID")
    space_id = fields.Int(attribute="SpaceID")
    category_id = fields.Int(attribute="CategoryID")
    name = fields.Str(attribute="EquipmentName") 
    brand = fields.Str(attribute="Brand")
    condition = fields.Str(attribute="Condition")
    rental_price = fields.Float(attribute="RentalPrice") 
    status = fields.Str(attribute="Status")
    purchase_date = fields.Str(attribute="PurchaseDate")
    created_at = fields.Str(attribute="CreatedAt")