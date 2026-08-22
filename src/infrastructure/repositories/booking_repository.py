from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.booking_model import BookingModel

class BookingRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> BookingModel:
        m = BookingModel(
            photographer_id=data.get('photographer_id'),
            space_id=data.get('space_id'),
            package_id=data.get('package_id'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status'),
            total_price=data.get('total_price'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[BookingModel]:
        return self.session.query(BookingModel).filter_by(id=id).first()

    def list(self) -> List[BookingModel]:
        return self.session.query(BookingModel).all()

    def update(self, data) -> BookingModel:
        m = self.session.query(BookingModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(BookingModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
