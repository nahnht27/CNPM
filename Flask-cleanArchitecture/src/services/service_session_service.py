from datetime import datetime
from typing import List


class ServiceSessionService:

    def __init__(self, repository):
        self.repository = repository

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_session(self, **data):

        booking_id = data.get('booking_id')

        if not booking_id:
            raise ValueError('booking_id là bắt buộc')

        # Mỗi booking chỉ có một ServiceSession
        existing = self.repository.get_by_booking_id(booking_id)

        if existing:
            return existing

        # Session mới chưa check-in
        data.setdefault('status', 'pending')

        return self.repository.add(data)

    # ==========================================================
    # GET BY ID
    # ==========================================================

    def get_session(self, session_id: int):

        return self.repository.get_by_id(session_id)

    # ==========================================================
    # GET BY BOOKING
    # ==========================================================

    def get_session_by_booking(self, booking_id: int):

        return self.repository.get_by_booking_id(booking_id)

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list_sessions(self) -> List:

        return self.repository.list()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_session(self, session_id: int, **data):

        return self.repository.update(
            session_id,
            data
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_session(self, session_id: int):

        return self.repository.delete(session_id)

    # ==========================================================
    # CHECK-IN
    # ==========================================================

    def check_in(
        self,
        booking_id: int,
        check_in_method=None,
        notes=None
    ):

        session = self.repository.get_by_booking_id(
            booking_id
        )

        if not session:
            return None, 'Không tìm thấy ServiceSession'

        if session.status == 'completed':
            return None, 'ServiceSession đã hoàn thành'

        if session.status == 'checked_in':
            return None, 'Booking đã check-in'

        if session.check_in_time:
            return None, 'Booking đã check-in'

        now = datetime.now()

        data = {
            'check_in_time': now,
            'check_in_method': check_in_method,
            'notes': notes,
            'status': 'checked_in'
        }

        session = self.repository.update(
            session.id,
            data
        )

        return session, None

    # ==========================================================
    # CHECK-OUT
    # ==========================================================

    def check_out(
        self,
        booking_id: int,
        notes=None
    ):

        session = self.repository.get_by_booking_id(
            booking_id
        )

        if not session:
            return None, 'Không tìm thấy ServiceSession'

        if session.status != 'checked_in':
            return None, 'ServiceSession chưa check-in'

        if not session.check_in_time:
            return None, 'Không xác định được thời gian check-in'

        if session.check_out_time:
            return None, 'Booking đã check-out'

        now = datetime.now()

        duration = int(
            (
                now - session.check_in_time
            ).total_seconds() / 60
        )

        data = {
            'check_out_time': now,
            'actual_duration_minutes': max(duration, 0),
            'status': 'completed'
        }

        if notes is not None:
            data['notes'] = notes

        session = self.repository.update(
            session.id,
            data
        )

        return session, None