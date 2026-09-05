
from typing import List
from datetime import datetime


class BookingService:
    def __init__(self, repository):
        self.repository = repository

    # ==========================================================
    # PHOTOGRAPHER BOOKING
    # ==========================================================

    def create_booking(self, **data):
        if data.get('start_time') >= data.get('end_time'):
            raise ValueError('Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc')

        return self.repository.add(data)

    def get_booking(self, id: int):
        return self.repository.get_by_id(id)

    def list_bookings(self) -> List:
        return self.repository.list()

    def update_booking(self, id: int, **data):
        if data.get('start_time') and data.get('end_time'):
            if data['start_time'] >= data['end_time']:
                raise ValueError(
                    'Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc'
                )

        return self.repository.update(id, data)

    def delete_booking(self, id: int):
        return self.repository.delete(id)

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
            return None, 'Booking không tồn tại hoặc không thuộc provider này'

        if booking.status != 'pending':
            return None, (
                f'Không thể xác nhận booking đang ở trạng thái '
                f'{booking.status}'
            )

        booking.status = 'confirmed'

        return self.repository.update(
            booking_id,
            {'status': 'confirmed'}
        ), None

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
            return None, 'Booking không tồn tại hoặc không thuộc provider này'

        if booking.status != 'pending':
            return None, (
                f'Không thể từ chối booking đang ở trạng thái '
                f'{booking.status}'
            )

        booking.status = 'cancelled'

        return self.repository.update(
            booking_id,
            {'status': 'cancelled'}
        ), None

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
            return None, 'Booking không tồn tại hoặc không thuộc provider này'

        if booking.status != 'confirmed':
            return None, (
                'Chỉ booking đã confirmed mới được check-in'
            )

        now = datetime.now()

        if now < booking.start_time:
            return None, 'Chưa đến thời gian bắt đầu booking'

        if now > booking.end_time:
            return None, 'Booking đã quá thời gian kết thúc'

        return self.repository.update(
            booking_id,
            {'status': 'checked_in'}
        ), None

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
            return None, 'Booking không tồn tại hoặc không thuộc provider này'

        if booking.status != 'checked_in':
            return None, (
                'Chỉ booking đã check-in mới được check-out'
            )

        return self.repository.update(
            booking_id,
            {'status': 'completed'}
        ), None

