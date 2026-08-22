from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.creative_space_model import CreativeSpaceModel

class CreativeSpaceRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> CreativeSpaceModel:
        m = CreativeSpaceModel(
            provider_id=data.get('provider_id'),
            name=data.get('name'),
            category_id=data.get('category_id'),
            description=data.get('description'),
            size_sqm=data.get('size_sqm'),
            max_capacity=data.get('max_capacity'),
            operating_hours=data.get('operating_hours'),
            pricing_model=data.get('pricing_model'),
            base_price=data.get('base_price'),
            status=data.get('status'),
            address=data.get('address'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[CreativeSpaceModel]:
        return self.session.query(CreativeSpaceModel).filter_by(id=id).first()

    def list(self) -> List[CreativeSpaceModel]:
        return self.session.query(CreativeSpaceModel).all()

    def update(self, data) -> CreativeSpaceModel:
        m = self.session.query(CreativeSpaceModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(CreativeSpaceModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
