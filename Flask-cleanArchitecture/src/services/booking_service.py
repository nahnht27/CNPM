from typing import List
from datetime import datetime


class BookingService:
    def __init__(
        self,
        repository,
        service_session_repository=None,
        invoice_repository=None,
        payment_repository=None
    ):
        self.repository = repository
        self.service_session_repository = service_session_repository
        self.invoice_repository = invoice_repository
        self.payment_repository = payment_repository

    # ==========================================================
    # PHOTOGRAPHER BOOKING
    # ==========================================================

    def create_booking(self, **data):

        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:

            if start_time >= end_time:
                raise ValueError(
                    'Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc'
                )

        # Booking mới luôn bắt đầu ở trạng thái pending
        data['status'] = 'pending'

        return self.repository.add(data)

    # ==========================================================
    # LẤY BOOKING CỦA PHOTOGRAPHER
    # ==========================================================

    def get_booking(
        self,
        id: int,
        photographer_id: int
    ):

        # Chỉ lấy booking nếu booking thuộc photographer hiện tại
        return self.repository.get_by_id_and_photographer(
            booking_id=id,
            photographer_id=photographer_id
        )

    def list_bookings(
        self,
        photographer_id=None
    ) -> List:

        return self.repository.list(
            photographer_id=photographer_id
        )

    # ==========================================================
    # UPDATE BOOKING CỦA PHOTOGRAPHER
    # ==========================================================

    def update_booking(
        self,
        id: int,
        photographer_id: int,
        **data
    ):

        # ------------------------------------------------------
        # KIỂM TRA OWNERSHIP
        # ------------------------------------------------------

        booking = self.repository.get_by_id_and_photographer(
            booking_id=id,
            photographer_id=photographer_id
        )

        if not booking:
            return None

        # ------------------------------------------------------
        # Không cho Photographer tự thay đổi trạng thái
        # vận hành của Booking
        # ------------------------------------------------------

        if 'status' in data:

            new_status = data['status']

            if new_status in {
                'confirmed',
                'checked_in',
                'completed'
            }:
                raise ValueError(
                    'Không thể thay đổi trạng thái booking '
                    f'sang {new_status}. '
                    'Trạng thái này phải được xử lý bởi Provider.'
                )

            # Photographer chỉ được hủy booking
            if new_status == 'cancelled':

                if booking.status != 'pending':
                    raise ValueError(
                        'Chỉ booking đang chờ xác nhận mới '
                        'có thể hủy.'
                    )

        # ------------------------------------------------------
        # Kiểm tra thời gian
        # ------------------------------------------------------

        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:

            if start_time >= end_time:
                raise ValueError(
                    'Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc'
                )

        return self.repository.update(
            id,
            data
        )

    # ==========================================================
    # DELETE BOOKING CỦA PHOTOGRAPHER
    # ==========================================================

    def delete_booking(
        self,
        id: int,
        photographer_id: int
    ):

        # ------------------------------------------------------
        # KIỂM TRA OWNERSHIP
        # ------------------------------------------------------

        booking = self.repository.get_by_id_and_photographer(
            booking_id=id,
            photographer_id=photographer_id
        )

        if not booking:
            return False

        try:

            self.repository.session.delete(booking)
            self.repository.session.commit()

            return True

        except Exception:

            self.repository.session.rollback()
            raise

    # ==========================================================
    # PROVIDER BOOKING MANAGEMENT
    # ==========================================================

    def list_provider_bookings(
        self,
        provider_id: int,
        status=None,
        date=None,
        space_id=None
    ):

        rows = self.repository.get_provider_bookings(
            provider_id=provider_id,
            status=status,
            date=date,
            space_id=space_id
        )

        result = []

        for booking, provider_id_value, space_name in rows:

            booking.provider_id = provider_id_value
            booking.space_name = space_name

            result.append(booking)

        return result

    def get_provider_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        row = self.repository.get_provider_booking(
            provider_id,
            booking_id
        )

        if not row:
            return None

        booking, provider_id_value, space_name = row

        booking.provider_id = provider_id_value
        booking.space_name = space_name

        return booking

    def _get_owned_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        return self.get_provider_booking(
            provider_id,
            booking_id
        )

    # ==========================================================
    # CONFIRM BOOKING
    # ==========================================================

    def confirm_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        booking = self._get_owned_booking(
            provider_id,
            booking_id
        )

        if not booking:
            return None, (
                'Booking không tồn tại hoặc không thuộc provider này'
            )

        if booking.status != 'pending':
            return None, (
                f'Không thể xác nhận booking đang ở trạng thái '
                f'{booking.status}'
            )

        # ------------------------------------------------------
        # 1. Confirm Booking
        # ------------------------------------------------------

        updated_booking = self.repository.update(
            booking_id,
            {
                'status': 'confirmed'
            }
        )

        # ------------------------------------------------------
        # 2. Tạo ServiceSession
        # ------------------------------------------------------

        if self.service_session_repository:

            existing_session = (
                self.service_session_repository
                .get_by_booking_id(booking_id)
            )

            if not existing_session:

                self.service_session_repository.add({
                    'booking_id': booking_id,
                    'status': 'pending'
                })

        # ------------------------------------------------------
        # 3. Tạo Invoice
        # ------------------------------------------------------

        if (
            self.service_session_repository
            and self.invoice_repository
        ):

            service_session = (
                self.service_session_repository
                .get_by_booking_id(booking_id)
            )

            if service_session:

                existing_invoice = (
                    self.invoice_repository
                    .get_by_session_id(service_session.id)
                )

                if not existing_invoice:

                    subtotal = (
                        updated_booking.total_price or 0
                    )

                    self.invoice_repository.add({
                        'session_id': service_session.id,
                        'invoice_number':
                            f'INV-{booking_id:06d}',
                        'subtotal': subtotal,
                        'discount_amount': 0,
                        'tax_amount': 0,
                        'total_amount': subtotal,
                        'issued_at': datetime.now()
                    })

        return updated_booking, None

    # ==========================================================
    # REJECT BOOKING
    # ==========================================================

    def reject_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        booking = self._get_owned_booking(
            provider_id,
            booking_id
        )

        if not booking:
            return None, (
                'Booking không tồn tại hoặc không thuộc provider này'
            )

        if booking.status != 'pending':
            return None, (
                f'Không thể từ chối booking đang ở trạng thái '
                f'{booking.status}'
            )

        return self.repository.update(
            booking_id,
            {
                'status': 'cancelled'
            }
        ), None

    # ==========================================================
    # CHECK-IN
    # ==========================================================

    def check_in_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        booking = self._get_owned_booking(
            provider_id,
            booking_id
        )

        if not booking:
            return None, (
                'Booking không tồn tại hoặc không thuộc provider này'
            )

        if booking.status != 'confirmed':
            return None, (
                'Chỉ booking đã confirmed mới được check-in'
            )

        now = datetime.now()

        # ------------------------------------------------------
        # Kiểm tra thời gian
        # ------------------------------------------------------

        if now < booking.start_time:
            return None, (
                'Chưa đến thời gian bắt đầu booking'
            )

        if now > booking.end_time:
            return None, (
                'Booking đã quá thời gian kết thúc'
            )

        # ------------------------------------------------------
        # KIỂM TRA SERVICE SESSION
        # ------------------------------------------------------

        service_session = None

        if self.service_session_repository:

            service_session = (
                self.service_session_repository
                .get_by_booking_id(booking_id)
            )

            if not service_session:
                return None, (
                    'Không tìm thấy ServiceSession'
                )

        # ------------------------------------------------------
        # KIỂM TRA INVOICE
        # ------------------------------------------------------

        invoice = None

        if self.invoice_repository:

            if not service_session:
                return None, (
                    'Không thể xác định ServiceSession '
                    'của booking'
                )

            invoice = (
                self.invoice_repository
                .get_by_session_id(service_session.id)
            )

            if not invoice:
                return None, (
                    'Không tìm thấy Invoice'
                )

        # ------------------------------------------------------
        # KIỂM TRA PAYMENT
        # ------------------------------------------------------

        if self.payment_repository:

            if not invoice:
                return None, (
                    'Không thể xác định Invoice '
                    'của booking'
                )

            payment = (
                self.payment_repository
                .get_by_invoice_id(invoice.id)
            )

            if not payment:
                return None, (
                    'Booking chưa thanh toán, '
                    'không thể check-in'
                )

            if payment.status != 'Thành công':
                return None, (
                    'Thanh toán chưa thành công, '
                    'không thể check-in'
                )

        # ------------------------------------------------------
        # UPDATE SERVICE SESSION
        # ------------------------------------------------------

        if service_session:

            self.service_session_repository.update(
                service_session.id,
                {
                    'check_in_time': now,
                    'status': 'checked_in'
                }
            )

        # ------------------------------------------------------
        # UPDATE BOOKING
        # ------------------------------------------------------

        updated_booking = self.repository.update(
            booking_id,
            {
                'status': 'checked_in'
            }
        )

        return updated_booking, None

    # ==========================================================
    # CHECK-OUT
    # ==========================================================

    def check_out_booking(
        self,
        provider_id: int,
        booking_id: int
    ):

        booking = self._get_owned_booking(
            provider_id,
            booking_id
        )

        if not booking:
            return None, (
                'Booking không tồn tại hoặc không thuộc provider này'
            )

        if booking.status != 'checked_in':
            return None, (
                'Chỉ booking đã check-in mới được check-out'
            )

        # ------------------------------------------------------
        # SERVICE SESSION
        # ------------------------------------------------------

        if (
            self.service_session_repository
            and self.invoice_repository
        ):

            service_session = (
                self.service_session_repository
                .get_by_booking_id(booking_id)
            )

            if service_session:

                existing_invoice = (
                    self.invoice_repository
                    .get_by_session_id(
                        service_session.id
                    )
                )

                if not existing_invoice:

                    # SỬA LỖI:
                    # updated_booking chưa tồn tại ở thời điểm này.
                    subtotal = (
                        booking.total_price or 0
                    )

                    self.invoice_repository.add({
                        'session_id': service_session.id,
                        'invoice_number':
                            f'INV-{booking_id:06d}',
                        'subtotal': subtotal,
                        'discount_amount': 0,
                        'tax_amount': 0,
                        'total_amount': subtotal,
                        'issued_at': datetime.now()
                    })

                # ==================================================
                # LẤY INVOICE SAU KHI TẠO
                # ==================================================

                invoice = (
                    self.invoice_repository
                    .get_by_session_id(
                        service_session.id
                    )
                )

                if invoice:
                    booking.invoice_id = invoice.id

        # ------------------------------------------------------
        # UPDATE BOOKING
        # ------------------------------------------------------

        updated_booking = self.repository.update(
            booking_id,
            {
                'status': 'completed'
            }
        )

        return updated_booking, None