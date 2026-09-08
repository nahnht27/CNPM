from typing import List, Optional
from sqlalchemy import or_

from infrastructure.models.booking_model import BookingModel
from infrastructure.models.creative_space_model import CreativeSpaceModel
from infrastructure.models.service_provider_model import ServiceProviderModel
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
    # HELPER: PARSE BANK INFO
    # ==========================================================

    def _build_payment_info(self, provider):
        """
        Tạo payment_info từ ServiceProviderModel.

        ServiceProviders:
            Bank_Info
            QRCodeUrl

        Ví dụ Bank_Info:

            Ngân hàng: Vietcombank |
            STK: 0123456789 |
            Chủ TK: NGUYEN VAN A

        Kết quả:

            {
                "bank_info": "...",
                "bank_name": "Vietcombank",
                "account_number": "0123456789",
                "account_name": "NGUYEN VAN A",
                "qr_code_url": "..."
            }
        """

        if not provider:
            return {
                "bank_info": None,
                "bank_name": None,
                "account_number": None,
                "account_name": None,
                "qr_code_url": None
            }

        bank_info = provider.bank_info or ""

        bank_name = None
        account_number = None
        account_name = None

        # ------------------------------------------------------
        # Parse Bank_Info
        # ------------------------------------------------------

        for part in bank_info.split("|"):

            key, separator, value = part.partition(":")

            if not separator:
                continue

            key = key.strip().lower()
            value = value.strip()

            if key in (
                "ngân hàng",
                "ngan hang",
                "bank",
                "bank name"
            ):
                bank_name = value

            elif key in (
                "stk",
                "số tài khoản",
                "so tai khoan",
                "account",
                "account number"
            ):
                account_number = value

            elif key in (
                "chủ tk",
                "chủ tài khoản",
                "chu tk",
                "chu tai khoan",
                "account name",
                "name"
            ):
                account_name = value

        # ------------------------------------------------------
        # Trường hợp Bank_Info không theo format key:value
        #
        # Ví dụ:
        # Vietcombank - 0123456789 - NGUYEN VAN A
        # ------------------------------------------------------

        if (
            not bank_name
            and not account_number
            and not account_name
            and bank_info
        ):

            parts = [
                item.strip()
                for item in bank_info.split("-")
                if item.strip()
            ]

            if len(parts) >= 1:
                bank_name = parts[0]

            if len(parts) >= 2:
                account_number = parts[1]

            if len(parts) >= 3:
                account_name = parts[2]

        return {
            "bank_info": bank_info or None,
            "bank_name": bank_name,
            "account_number": account_number,
            "account_name": account_name,
            "qr_code_url": provider.qr_code_url or None
        }

    # ==========================================================
    # HELPER: GẮN THÔNG TIN THANH TOÁN PROVIDER
    # ==========================================================

    def _attach_provider_payment_info(
        self,
        booking
    ):
        """
        Gắn payment_info vào Booking.

        Quan hệ:

            Booking
                |
                | SpaceID
                v
            CreativeSpaces
                |
                | ProviderID
                v
            ServiceProviders
                |
                +-- Bank_Info
                +-- QRCodeUrl
        """

        if not booking:
            return booking

        provider = (
            self.session.query(ServiceProviderModel)
            .join(
                CreativeSpaceModel,
                CreativeSpaceModel.provider_id ==
                ServiceProviderModel.id
            )
            .filter(
                CreativeSpaceModel.id ==
                booking.space_id
            )
            .first()
        )

        booking.payment_info = self._build_payment_info(
            provider
        )

        return booking

    # ==========================================================
    # HELPER: ATTACH BOOKING DATA
    # ==========================================================

    def _attach_booking_extra_data(
        self,
        booking
    ):
        """
        Gắn toàn bộ dữ liệu động cần thiết cho Booking response.

        Bao gồm:
            - invoice_id
            - payment_info
        """

        if not booking:
            return booking

        self._attach_invoice_id(booking)
        self._attach_provider_payment_info(booking)

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

            # Booking mới vẫn có thể lấy được thông tin
            # thanh toán của provider thông qua SpaceID.
            self._attach_provider_payment_info(model)

            return model

        except Exception:

            self.session.rollback()
            raise

    # ==========================================================
    # GET BOOKING BY ID
    # ==========================================================

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

        return self._attach_booking_extra_data(
            booking
        )

    # ==========================================================
    # LẤY BOOKING THEO PHOTOGRAPHER
    # ==========================================================

    def get_by_id_and_photographer(
        self,
        booking_id: int,
        photographer_id: int
    ) -> Optional[BookingModel]:
        """
        Chỉ cho phép Photographer xem Booking của chính mình.
        """

        booking = (
            self.session.query(BookingModel)
            .filter(
                BookingModel.id == booking_id,
                BookingModel.photographer_id == photographer_id
            )
            .first()
        )

        return self._attach_booking_extra_data(
            booking
        )

    # ==========================================================
    # LIST BOOKING
    # ==========================================================

    def list(
        self,
        photographer_id: Optional[int] = None
    ) -> List[BookingModel]:

        query = self.session.query(BookingModel)

        # Nếu có photographer_id thì bắt buộc lọc
        # theo photographer đó.
        if photographer_id is not None:
            query = query.filter(
                BookingModel.photographer_id ==
                photographer_id
            )

        bookings = query.all()

        for booking in bookings:

            self._attach_booking_extra_data(
                booking
            )

        return bookings

    # ==========================================================
    # CHECK BOOKING TRÙNG THỜI GIAN
    # ==========================================================

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
                    BookingModel.photographer_id ==
                    photographer_id,

                    BookingModel.space_id ==
                    space_id
                ),

                BookingModel.start_time <
                end_time,

                BookingModel.end_time >
                start_time
            )
            .all()
        )

        for booking in bookings:

            self._attach_booking_extra_data(
                booking
            )

        return bookings

    # ==========================================================
    # UPDATE
    # ==========================================================

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

            # Sau khi update, lấy lại toàn bộ
            # dữ liệu dynamic.
            self._attach_booking_extra_data(
                booking
            )

            return booking

        except Exception:

            self.session.rollback()
            raise

    # ==========================================================
    # DELETE
    # ==========================================================

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
                BookingModel.status ==
                status
            )

        if space_id:

            query = query.filter(
                BookingModel.space_id ==
                space_id
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

        for (
            booking,
            provider_id_value,
            space_name
        ) in rows:

            self._attach_booking_extra_data(
                booking
            )

            booking.provider_id = (
                provider_id_value
            )

            booking.space_name = (
                space_name
            )

            result.append(
                (
                    booking,
                    provider_id_value,
                    space_name
                )
            )

        return result

    # ==========================================================
    # PROVIDER GET BOOKING
    # ==========================================================

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
                BookingModel.id ==
                booking_id,

                CreativeSpaceModel.provider_id ==
                provider_id
            )
            .first()
        )

        if not row:
            return None

        (
            booking,
            provider_id_value,
            space_name
        ) = row

        self._attach_booking_extra_data(
            booking
        )

        booking.provider_id = (
            provider_id_value
        )

        booking.space_name = (
            space_name
        )

        return (
            booking,
            provider_id_value,
            space_name
        )

    # ==========================================================
    # GET PROVIDER SPACE IDS
    # ==========================================================

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

