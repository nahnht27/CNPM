from typing import List, Optional

from infrastructure.databases.factory_database import (
    FactoryDatabase as db_factory
)

from infrastructure.models.service_provider_model import (
    ServiceProviderModel
)


class ServiceProviderRepository:

    def __init__(self, session=None):

        self.session = (
            session
            or db_factory.get_database("POSTGRES").session
        )

    # =====================================================
    # CREATE
    # =====================================================

    def add(self, data) -> ServiceProviderModel:

        model = ServiceProviderModel(
            user_id=data.get("user_id"),

            business_name=data.get(
                "business_name"
            ),

            tax_code=data.get(
                "tax_code"
            ),

            business_address=data.get(
                "business_address"
            ),

            license_url=data.get(
                "license_url"
            ),

            # QR thanh toán
            qr_code_url=data.get(
                "qr_code_url"
            ),

            verification_status=data.get(
                "verification_status"
            ),

            approved_at=data.get(
                "approved_at"
            ),

            bank_info=data.get(
                "bank_info"
            ),

            created_at=data.get(
                "created_at"
            )
        )

        try:

            self.session.add(model)

            self.session.commit()

            self.session.refresh(model)

            return model

        except Exception:

            self.session.rollback()

            raise

    # =====================================================
    # GET BY ID
    # =====================================================

    def get_by_id(
        self,
        id: int
    ) -> Optional[ServiceProviderModel]:

        return (
            self.session
            .query(ServiceProviderModel)
            .filter_by(id=id)
            .first()
        )

    # =====================================================
    # GET ALL
    # =====================================================

    def list(self) -> List[ServiceProviderModel]:

        return (
            self.session
            .query(ServiceProviderModel)
            .all()
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        data
    ) -> ServiceProviderModel:

        provider_id = data.get("id")

        model = (
            self.session
            .query(ServiceProviderModel)
            .filter_by(id=provider_id)
            .first()
        )

        if not model:

            raise ValueError(
                "ServiceProvider not found"
            )

        # -------------------------------------------------
        # Các field được phép cập nhật từ profile
        # -------------------------------------------------

        allowed_fields = {
            "business_name",
            "tax_code",
            "business_address",
            "license_url",
            "verification_status",
            "approved_at",
            "bank_info",
            "qr_code_url"
        }

        try:

            for key, value in data.items():

                # Không bao giờ update primary key
                if key == "id":
                    continue

                # Chỉ update field hợp lệ
                if key not in allowed_fields:
                    continue

                # Đảm bảo field thực sự tồn tại trên model
                if hasattr(model, key):

                    setattr(
                        model,
                        key,
                        value
                    )

            self.session.commit()

            self.session.refresh(model)

            return model

        except Exception:

            self.session.rollback()

            raise

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        id: int
    ) -> None:

        model = (
            self.session
            .query(ServiceProviderModel)
            .filter_by(id=id)
            .first()
        )

        if not model:
            return

        try:

            self.session.delete(model)

            self.session.commit()

        except Exception:

            self.session.rollback()

            raise