from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.auth import LoginUserRequestSchema, LoginUserResponseSchema, RigisterUserRequestSchema, RigisterUserResponseSchema
from api.schemas.role import RoleRequestSchema, RoleResponseSchema
from api.schemas.service_provider import ServiceProviderRequestSchema, ServiceProviderResponseSchema
from api.schemas.post import PostRequestSchema, PostResponseSchema
from api.schemas.post_comment import PostCommentRequestSchema, PostCommentResponseSchema
from api.schemas.promotion import PromotionRequestSchema, PromotionResponseSchema
from api.schemas.package_detail import PackageDetailRequestSchema, PackageDetailResponseSchema
from api.schemas.service_package import ServicePackageRequestSchema, ServicePackageResponseSchema
from api.schemas.notification import NotificationRequestSchema, NotificationResponseSchema
from api.schemas.review import ReviewRequestSchema, ReviewResponseSchema
from api.schemas.complaint import ComplaintRequestSchema, ComplaintResponseSchema
from api.schemas.ai_interaction_log import AIInteractionLogRequestSchema, AIInteractionLogResponseSchema
from api.schemas.ai_configuration import AIConfigurationRequestSchema, AIConfigurationResponseSchema
from api.schemas.workshop import WorkshopRequestSchema, WorkshopResponseSchema
from api.schemas.workshop_registration import WorkshopRegistrationRequestSchema, WorkshopRegistrationResponseSchema
from api.schemas.user import UserResponseSchema, UserUpdateRequestSchema
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema
from api.schemas.invoice import InvoiceRequestSchema, InvoiceResponseSchema
from api.schemas.payment import PaymentRequestSchema, PaymentResponseSchema
from api.schemas.equipment import EquipmentRequestSchema, EquipmentResponseSchema
from api.schemas.creative_space import CreativeSpaceRequestSchema, CreativeSpaceResponseSchema
from api.schemas.category import CategoryRequestSchema, CategoryResponseSchema

#bổ sung các schema
from api.schemas.amenity import (
    AmenityRequestSchema,
    AmenityResponseSchema
)

from api.schemas.booking_equipment import (
    BookingEquipmentRequestSchema,
    BookingEquipmentResponseSchema
)

from api.schemas.consumable import (
    ConsumableRequestSchema,
    ConsumableResponseSchema
)

from api.schemas.equipment_maintenance_log import (
    EquipmentMaintenanceLogRequestSchema,
    EquipmentMaintenanceLogResponseSchema
)

from api.schemas.invoice_detail import (
    InvoiceDetailRequestSchema,
    InvoiceDetailResponseSchema
)

from api.schemas.service_session import (
    ServiceSessionRequestSchema,
    ServiceSessionResponseSchema
)

from api.schemas.session_equipment_usage import (
    SessionEquipmentUsageRequestSchema,
    SessionEquipmentUsageResponseSchema
)

from api.schemas.session_consumable_usage import (
    SessionConsumableUsageRequestSchema,
    SessionConsumableUsageResponseSchema
)

from api.schemas.space_amenity import (
    SpaceAmenityRequestSchema,
    SpaceAmenityResponseSchema
)

from api.schemas.space_image import (
    SpaceImageRequestSchema,
    SpaceImageResponseSchema
)

spec = APISpec(
    title="Film Photography Community Platform API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Đăng ký schema để tự động sinh model
spec.components.schema("LoginUserRequest", schema= LoginUserRequestSchema)
spec.components.schema("LoginUserResponse", schema= LoginUserResponseSchema)
spec.components.schema("RigisterUserRequest", schema= RigisterUserRequestSchema)
spec.components.schema("RigisterUserResponse", schema= RigisterUserResponseSchema)
spec.components.schema("RoleRequest", schema=RoleRequestSchema)
spec.components.schema("RoleResponse", schema=RoleResponseSchema)
spec.components.schema("ServiceProviderRequest", schema=ServiceProviderRequestSchema)
spec.components.schema("ServiceProviderResponse", schema=ServiceProviderResponseSchema)
spec.components.schema("PostRequest", schema=PostRequestSchema)
spec.components.schema("PostResponse", schema=PostResponseSchema)
spec.components.schema("PostCommentRequest", schema=PostCommentRequestSchema)
spec.components.schema("PostCommentResponse", schema=PostCommentResponseSchema)
spec.components.schema("PromotionRequest", schema=PromotionRequestSchema)
spec.components.schema("PromotionResponse", schema=PromotionResponseSchema)
spec.components.schema("PackageDetailRequest", schema=PackageDetailRequestSchema)
spec.components.schema("PackageDetailResponse", schema=PackageDetailResponseSchema)
spec.components.schema("ServicePackageRequest", schema=ServicePackageRequestSchema)
spec.components.schema("ServicePackageResponse", schema=ServicePackageResponseSchema)
spec.components.schema("NotificationRequest", schema=NotificationRequestSchema)
spec.components.schema("NotificationResponse", schema=NotificationResponseSchema)
spec.components.schema("ReviewRequest", schema=ReviewRequestSchema)
spec.components.schema("ReviewResponse", schema=ReviewResponseSchema)
spec.components.schema("ComplaintRequest", schema=ComplaintRequestSchema)
spec.components.schema("ComplaintResponse", schema=ComplaintResponseSchema)
spec.components.schema("AIInteractionLogRequest", schema=AIInteractionLogRequestSchema)
spec.components.schema("AIInteractionLogResponse", schema=AIInteractionLogResponseSchema)
spec.components.schema("AIConfigurationRequest", schema=AIConfigurationRequestSchema)
spec.components.schema("AIConfigurationResponse", schema=AIConfigurationResponseSchema)
spec.components.schema("WorkshopRequest", schema=WorkshopRequestSchema)
spec.components.schema("WorkshopResponse", schema=WorkshopResponseSchema)
spec.components.schema("WorkshopRegistrationRequest", schema=WorkshopRegistrationRequestSchema)
spec.components.schema("WorkshopRegistrationResponse", schema=WorkshopRegistrationResponseSchema)
spec.components.schema("UserRequest", schema=UserUpdateRequestSchema)
spec.components.schema("UserResponse", schema=UserResponseSchema)
spec.components.schema("BookingRequest", schema=BookingRequestSchema)
spec.components.schema("BookingResponse", schema=BookingResponseSchema)
spec.components.schema("InvoiceRequest", schema=InvoiceRequestSchema)
spec.components.schema("InvoiceResponse", schema=InvoiceResponseSchema)
spec.components.schema("PaymentRequest", schema=PaymentRequestSchema)
spec.components.schema("PaymentResponse", schema=PaymentResponseSchema)
spec.components.schema("EquipmentRequest", schema=EquipmentRequestSchema)
spec.components.schema("EquipmentResponse", schema=EquipmentResponseSchema)
spec.components.schema("CreativeSpaceRequest", schema=CreativeSpaceRequestSchema)
spec.components.schema("CreativeSpaceResponse", schema=CreativeSpaceResponseSchema)
spec.components.schema("CategoryRequest", schema=CategoryRequestSchema)
spec.components.schema("CategoryResponse", schema=CategoryResponseSchema)

#các schema bổ sung
spec.components.schema(
    "AmenityRequest",
    schema=AmenityRequestSchema
)

spec.components.schema(
    "AmenityResponse",
    schema=AmenityResponseSchema
)

spec.components.schema(
    "BookingEquipmentRequest",
    schema=BookingEquipmentRequestSchema
)

spec.components.schema(
    "BookingEquipmentResponse",
    schema=BookingEquipmentResponseSchema
)

spec.components.schema(
    "ConsumableRequest",
    schema=ConsumableRequestSchema
)

spec.components.schema(
    "ConsumableResponse",
    schema=ConsumableResponseSchema
)

spec.components.schema(
    "EquipmentMaintenanceLogRequest",
    schema=EquipmentMaintenanceLogRequestSchema
)

spec.components.schema(
    "EquipmentMaintenanceLogResponse",
    schema=EquipmentMaintenanceLogResponseSchema
)

spec.components.schema(
    "InvoiceDetailRequest",
    schema=InvoiceDetailRequestSchema
)

spec.components.schema(
    "InvoiceDetailResponse",
    schema=InvoiceDetailResponseSchema
)

spec.components.schema(
    "ServiceSessionRequest",
    schema=ServiceSessionRequestSchema
)

spec.components.schema(
    "ServiceSessionResponse",
    schema=ServiceSessionResponseSchema
)

spec.components.schema(
    "SessionEquipmentUsageRequest",
    schema=SessionEquipmentUsageRequestSchema
)

spec.components.schema(
    "SessionEquipmentUsageResponse",
    schema=SessionEquipmentUsageResponseSchema
)

spec.components.schema(
    "SessionConsumableUsageRequest",
    schema=SessionConsumableUsageRequestSchema
)

spec.components.schema(
    "SessionConsumableUsageResponse",
    schema=SessionConsumableUsageResponseSchema
)

spec.components.schema(
    "SpaceAmenityRequest",
    schema=SpaceAmenityRequestSchema
)

spec.components.schema(
    "SpaceAmenityResponse",
    schema=SpaceAmenityResponseSchema
)

spec.components.schema(
    "SpaceImageRequest",
    schema=SpaceImageRequestSchema
)

spec.components.schema(
    "SpaceImageResponse",
    schema=SpaceImageResponseSchema
)