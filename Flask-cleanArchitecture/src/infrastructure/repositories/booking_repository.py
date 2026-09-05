from typing import List, Optional
from infrastructure.models.booking_model import BookingModel
from sqlalchemy import or_

class BookingRepository:
    def __init__(self, session):
        self.session = session

    def add(self, data) -> BookingModel:
        m = BookingModel(
            photographer_id=data.get('photographer_id'),
            space_id=data.get('space_id'),
            package_id=data.get('package_id'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status', 'pending'),
            total_price=data.get('total_price', 0),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, booking_id: int) -> Optional[BookingModel]:
        return self.session.query(BookingModel).filter(BookingModel.id == booking_id).first()

    def list(self) -> List[BookingModel]:
        return self.session.query(BookingModel).all()

    def get_bookings_by_time_range(self, photographer_id: int, space_id: int, start_time, end_time):
        return self.session.query(BookingModel).filter(
            or_(
                BookingModel.photographer_id == photographer_id,
                BookingModel.space_id == space_id
            ),
            BookingModel.start_time < end_time,
            BookingModel.end_time > start_time
        ).all()

    # --- BỔ SUNG HÀM UPDATE VÀ DELETE VÀO ĐÂY ---
    def update(self, booking_id: int, data: dict) -> Optional[BookingModel]:
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        # Tự động cập nhật các trường có trong dict data
        for key, value in data.items():
            if hasattr(booking, key) and value is not None:
                setattr(booking, key, value)

        self.session.commit()
        self.session.refresh(booking)
        return booking

    def delete(self, booking_id: int) -> bool:
        booking = self.get_by_id(booking_id)
        if not booking:
            return False
        self.session.delete(booking)
        self.session.commit()
        return True