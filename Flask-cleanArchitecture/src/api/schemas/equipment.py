from marshmallow import Schema, fields, EXCLUDE, pre_dump

# 1. Request Schema cho API Tạo/Cập nhật Thiết bị
class EquipmentRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Bỏ qua các field thừa nếu client gửi lên

    provider_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    name = fields.Str(required=True)
    space_id = fields.Int(required=False, allow_none=True)
    brand = fields.Str(required=False, allow_none=True)
    condition = fields.Str(required=False, allow_none=True)
    rental_price = fields.Float(required=False, allow_none=True)
    status = fields.Str(required=False, load_default="available")
    purchase_date = fields.Str(required=False, allow_none=True)


# 2. Response Schema chuẩn hóa trả về JSON cho Frontend
class EquipmentResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # Map tên cột DB (PascalCase) sang thuộc tính JSON chuẩn Frontend (snake_case)
    id = fields.Int(attribute="EquipmentID", data_key="id")
    provider_id = fields.Int(attribute="ProviderID", data_key="provider_id")
    space_id = fields.Int(attribute="SpaceID", data_key="space_id", allow_none=True)
    category_id = fields.Int(attribute="CategoryID", data_key="category_id")
    name = fields.Str(attribute="EquipmentName", data_key="name") 
    brand = fields.Str(attribute="Brand", allow_none=True)
    condition = fields.Str(attribute="Condition", allow_none=True)
    rental_price = fields.Float(attribute="RentalPrice", data_key="rental_price") 
    status = fields.Str(attribute="Status")
    purchase_date = fields.Str(attribute="PurchaseDate", allow_none=True)
    created_at = fields.Str(attribute="CreatedAt", allow_none=True)

    @pre_dump
    def normalize_equipment_data(self, data, **kwargs):
        """
        Xử lý linh hoạt cả khi Repo trả về ORM Model Object hoặc Dict raw query từ SQL
        """
        if isinstance(data, dict):
            # Fallback nếu dict sử dụng key dạng snake_case
            if 'EquipmentID' not in data and 'id' in data:
                data['EquipmentID'] = data['id']
            if 'EquipmentName' not in data and 'name' in data:
                data['EquipmentName'] = data['name']
            if 'RentalPrice' not in data and 'rental_price' in data:
                data['RentalPrice'] = data['rental_price']
            if 'ProviderID' not in data and 'provider_id' in data:
                data['ProviderID'] = data['provider_id']
            if 'CategoryID' not in data and 'category_id' in data:
                data['CategoryID'] = data['category_id']
            if 'SpaceID' not in data and 'space_id' in data:
                data['SpaceID'] = data['space_id']
            if 'Status' not in data and 'status' in data:
                data['Status'] = data['status']
                
            # Ép kiểu RentalPrice về float an toàn cho JS
            if 'RentalPrice' in data and data['RentalPrice'] is not None:
                data['RentalPrice'] = float(data['RentalPrice'])

        return data