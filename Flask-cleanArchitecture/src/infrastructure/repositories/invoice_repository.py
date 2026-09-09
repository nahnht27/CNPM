from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.invoice_model import InvoiceModel
from infrastructure.models.service_session_model import ServiceSessionModel
from infrastructure.models.booking_model import BookingModel
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.service_package_model import ServicePackageModel


class InvoiceRepository:

    def __init__(self, session=None):
        self.session = (
            session
            or db_factory.get_database('POSTGREE').session
        )

    # ==========================================================
    # HELPER: GẮN CHI TIẾT DỊCH VỤ VÀO INVOICE
    # ==========================================================

    def _attach_details(self, invoice: Optional[InvoiceModel]) -> Optional[InvoiceModel]:
        """
        Invoice -> ServiceSession -> Booking -> (CreativeSpace, ServicePackage)
        Gắn thêm booking_id và danh sách invoice_details vào Invoice object.
        """
        if not invoice:
            return None

        details = []
        booking_id = None

        if invoice.session_id:
            # Query ServiceSession từ session_id
            session_item = (
                self.session.query(ServiceSessionModel)
                .filter(ServiceSessionModel.id == invoice.session_id)
                .first()
            )

            if session_item and session_item.booking_id:
                booking_id = session_item.booking_id

                # Query Booking từ booking_id
                booking = (
                    self.session.query(BookingModel)
                    .filter(BookingModel.id == booking_id)
                    .first()
                )

                if booking:
                    # 1. Thêm Không gian Studio
                    if booking.space_id:
                        space = (
                            self.session.query(CreativeSpaceModel)
                            .filter(CreativeSpaceModel.id == booking.space_id)
                            .first()
                        )
                        space_name = space.name if space else f"Không gian #{booking.space_id}"
                        details.append({
                            "name": f"Thuê không gian: {space_name}",
                            "quantity": 1,
                            "amount": float(booking.total_price or 0)
                        })

                    # 2. Thêm Gói dịch vụ đi kèm (nếu có)
                    if booking.package_id:
                        package = (
                            self.session.query(ServicePackageModel)
                            .filter(ServicePackageModel.id == booking.package_id)
                            .first()
                        )
                        if package:
                            details.append({
                                "name": f"Gói dịch vụ: {package.name}",
                                "quantity": 1,
                                "amount": float(package.price or 0)
                            })

        # Gắn dynamic attributes để Marshmallow dump
        invoice.booking_id = booking_id
        invoice.invoice_details = details

        return invoice

    # ==========================================================
    # CREATE
    # ==========================================================

    def add(self, data) -> InvoiceModel:

        model = InvoiceModel(
            session_id=data.get('session_id'),
            invoice_number=data.get('invoice_number'),
            subtotal=data.get('subtotal'),
            discount_amount=data.get('discount_amount'),
            tax_amount=data.get('tax_amount'),
            total_amount=data.get('total_amount'),
            issued_at=data.get('issued_at')
        )

        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)

            return self._attach_details(model)

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # GET BY ID
    # ==========================================================

    def get_by_id(
        self,
        id: int
    ) -> Optional[InvoiceModel]:

        invoice = (
            self.session.query(InvoiceModel)
            .filter_by(id=id)
            .first()
        )

        return self._attach_details(invoice)

    # ==========================================================
    # GET BY SERVICE SESSION
    # ==========================================================

    def get_by_session_id(
        self,
        session_id: int
    ) -> Optional[InvoiceModel]:

        invoice = (
            self.session.query(InvoiceModel)
            .filter_by(session_id=session_id)
            .first()
        )

        return self._attach_details(invoice)

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list(self) -> List[InvoiceModel]:

        invoices = (
            self.session
            .query(InvoiceModel)
            .all()
        )

        for invoice in invoices:
            self._attach_details(invoice)

        return invoices

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        data
    ) -> Optional[InvoiceModel]:

        model = (
            self.session.query(InvoiceModel)
            .filter_by(id=data.get('id'))
            .first()
        )

        if not model:
            return None

        try:

            for key, value in data.items():

                if hasattr(model, key) and key != 'id':
                    setattr(model, key, value)

            self.session.commit()
            self.session.refresh(model)

            return self._attach_details(model)

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        id: int
    ) -> bool:

        model = (
            self.session.query(InvoiceModel)
            .filter_by(id=id)
            .first()
        )

        if not model:
            return False

        try:

            self.session.delete(model)
            self.session.commit()

            return True

        except Exception:
            self.session.rollback()
            raise