from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.review_model import ReviewModel

class ReviewRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> ReviewModel:
        m = ReviewModel(
            photographer_id=data.get('photographer_id'),
            booking_id=data.get('booking_id'),
            target_type=data.get('target_type'),
            target_id=data.get('target_id'),
            rating=data.get('rating'),
            comment=data.get('comment'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[ReviewModel]:
        return self.session.query(ReviewModel).filter_by(id=id).first()

    def list(self) -> List[ReviewModel]:
        return self.session.query(ReviewModel).all()

    def update(self, data) -> ReviewModel:
        m = self.session.query(ReviewModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(ReviewModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
