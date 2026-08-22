"bổ sung import Base để đảm bảo rằng các mô hình cơ sở dữ liệu được định nghĩa đúng cách "
"và có thể sử dụng các tính năng của SQLAlchemy."
import traceback

from infrastructure.databases.base import Base 
from infrastructure.databases.factory_database import FactoryDatabase


def register_models():
    """Import model modules to ensure SQLAlchemy metadata is populated.
    This is performed lazily to avoid heavy imports at module import time.
    """
    from infrastructure.models import (
        user_model,
        role_model,
        service_provider_model,
        category_model,
        creative_space_model,
        space_image_model,
        amenity_model,
        space_amenity_model,
        equipment_model,
        consumable_model,
        equipment_maintenance_log_model,
        booking_model,
        booking_equipment_model,
        service_session_model,
        session_equipment_usage_model,
        session_consumable_usage_model,
        invoice_model,
        invoice_detail_model,
        payment_model,
        service_package_model,
        package_detail_model,
        promotion_model,
        review_model,
        post_model,
        post_comment_model,
        workshop_model,
        workshop_registration_model,
        ai_interaction_log_model,
        ai_configuration_model,
        notification_model,
        complaint_model,
    )


def init_db(app):
    # Lazily register models, then initialize DB
    register_models()
    FactoryDatabase.get_database('POSTGREE').init_database(app)

