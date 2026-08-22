from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.promotion_model import PromotionModel

class PromotionRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> PromotionModel:
        m = PromotionModel(
            provider_id=data.get('provider_id'),
            package_id=data.get('package_id'),
            code=data.get('code'),
            discount_type=data.get('discount_type'),
            discount_value=data.get('discount_value'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            usage_limit=data.get('usage_limit'),
            status=data.get('status')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[PromotionModel]:
        return self.session.query(PromotionModel).filter_by(id=id).first()

    def list(self) -> List[PromotionModel]:
        return self.session.query(PromotionModel).all()

    def update(self, data) -> PromotionModel:
        m = self.session.query(PromotionModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(PromotionModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
