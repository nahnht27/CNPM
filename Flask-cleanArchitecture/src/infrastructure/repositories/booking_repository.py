from typing import List, Optional
from sqlalchemy import or_

from infrastructure.models.booking_model import BookingModel
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.service_session_model import ServiceSessionModel
from infrastructure.models.invoice_model import InvoiceModel


class BookingRepository:

    def __init__(self, session):
        self.session = session

    # ==========================================================
    # HELPER: GẮN INVOICE ID VÀO BOOKING
    # ==========================================================

    def _attach_invoice_id(self, booking):
        """
        Booking không có cột InvoiceID.

        Quan hệ:
            Booking
                -> ServiceSession
                -> Invoice

        Hàm này tìm Invoice tương ứng và gắn invoice_id
        vào object Booking để Service/Controller/Schema
        có thể trả về cho frontend.
        """

        if not booking:
            return booking

        service_session = (
            self.session.query(ServiceSessionModel)
            .filter(
                ServiceSessionModel.booking_id == booking.id
            )
            .first()
        )

        invoice_id = None

        if service_session:

            invoice = (
                self.session.query(InvoiceModel)
                .filter(
                    InvoiceModel.session_id == service_session.id
                )
                .first()
            )

            if invoice:
                invoice_id = invoice.id

        # BookingModel không có column invoice_id.
        # Gắn dynamic attribute để response có thể sử dụng.
        booking.invoice_id = invoice_id

        return booking

    # ==========================================================
    # PHOTOGRAPHER BOOKING
    # ==========================================================

    def add(self, data) -> BookingModel:

        model = BookingModel(
            photographer_id=data.get('photographer_id'),
            space_id=data.get('space_id'),
            package_id=data.get('package_id'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status', 'pending'),
            total_price=data.get('total_price', 0),
            created_at=data.get('created_at')
        )

        try:

            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)

            # Booking mới chưa có ServiceSession/Invoice
            model.invoice_id = None

            return model

        except Exception:

            self.session.rollback()
            raise

    def get_by_id(
        self,
        booking_id: int
    ) -> Optional[BookingModel]:

        booking = (
            self.session.query(BookingModel)
            .filter(
                BookingModel.id == booking_id
            )
            .first()
        )

        return self._attach_invoice_id(booking)

    def list(self, photographer_id: Optional[int] = None) -> List[BookingModel]:
        query = self.session.query(BookingModel)

        # Nếu có truyền photographer_id -> Lọc đúng theo user đó
        if photographer_id:
            query = query.filter(BookingModel.photographer_id == photographer_id)

        bookings = query.all()

        for booking in bookings:
            self._attach_invoice_id(booking)

        return bookings

    def get_bookings_by_time_range(
        self,
        photographer_id: int,
        space_id: int,
        start_time,
        end_time
    ):

        bookings = (
            self.session.query(BookingModel)
            .filter(
                or_(
                    BookingModel.photographer_id == photographer_id,
                    BookingModel.space_id == space_id
                ),
                BookingModel.start_time < end_time,
                BookingModel.end_time > start_time
            )
            .all()
        )

        for booking in bookings:
            self._attach_invoice_id(booking)

        return bookings

    def update(
        self,
        booking_id: int,
        data: dict
    ) -> Optional[BookingModel]:

        booking = self.get_by_id(
            booking_id
        )

        if not booking:
            return None

        try:

            for key, value in data.items():

                if (
                    hasattr(booking, key)
                    and value is not None
                ):
                    setattr(
                        booking,
                        key,
                        value
                    )

            self.session.commit()
            self.session.refresh(booking)

            # Sau khi update, lấy lại invoice_id
            self._attach_invoice_id(booking)

            return booking

        except Exception:

            self.session.rollback()
            raise

    def delete(
        self,
        booking_id: int
    ) -> bool:

        booking = self.get_by_id(
            booking_id
        )

        if not booking:
            return False

        try:

            self.session.delete(booking)
            self.session.commit()

            return True

        except Exception:

            self.session.rollback()
            raise

    # ==========================================================
    # PROVIDER BOOKING MANAGEMENT
    # ==========================================================

    def get_provider_bookings(
        self,
        provider_id: int,
        status: Optional[str] = None,
        date: Optional[str] = None,
        space_id: Optional[int] = None
    ):

        query = (
            self.session.query(
                BookingModel,
                CreativeSpaceModel.provider_id,
                CreativeSpaceModel.name
            )
            .join(
                CreativeSpaceModel,
                BookingModel.space_id ==
                CreativeSpaceModel.id
            )
            .filter(
                CreativeSpaceModel.provider_id ==
                provider_id
            )
        )

        if status:

            query = query.filter(
                BookingModel.status == status
            )

        if space_id:

            query = query.filter(
                BookingModel.space_id == space_id
            )

        if date:

            query = query.filter(
                BookingModel.start_time >=
                f'{date} 00:00:00',
                BookingModel.start_time <
                f'{date} 23:59:59'
            )

        query = query.order_by(
            BookingModel.start_time.desc()
        )

        rows = query.all()

        result = []

        for booking, provider_id_value, space_name in rows:

            self._attach_invoice_id(booking)

            booking.provider_id = provider_id_value
            booking.space_name = space_name

            result.append(
                (
                    booking,
                    provider_id_value,
                    space_name
                )
            )

        return result

    def get_provider_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        row = (
            self.session.query(
                BookingModel,
                CreativeSpaceModel.provider_id,
                CreativeSpaceModel.name
            )
            .join(
                CreativeSpaceModel,
                BookingModel.space_id ==
                CreativeSpaceModel.id
            )
            .filter(
                BookingModel.id == booking_id,
                CreativeSpaceModel.provider_id ==
                provider_id
            )
            .first()
        )

        if not row:
            return None

        booking, provider_id_value, space_name = row

        self._attach_invoice_id(booking)

        return (
            booking,
            provider_id_value,
            space_name
        )

    def get_provider_space_ids(
        self,
        provider_id: int
    ):

        return [
            row.id
            for row in (
                self.session.query(
                    CreativeSpaceModel.id
                )
                .filter(
                    CreativeSpaceModel.provider_id ==
                    provider_id
                )
                .all()
            )
        ]