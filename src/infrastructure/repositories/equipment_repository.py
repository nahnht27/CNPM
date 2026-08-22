from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.equipment_model import EquipmentModel

class EquipmentRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> EquipmentModel:
        m = EquipmentModel(
            provider_id=data.get('provider_id'),
            space_id=data.get('space_id'),
            category_id=data.get('category_id'),
            name=data.get('name'),
            brand=data.get('brand'),
            condition=data.get('condition'),
            rental_price=data.get('rental_price'),
            status=data.get('status'),
            purchase_date=data.get('purchase_date'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[EquipmentModel]:
        return self.session.query(EquipmentModel).filter_by(id=id).first()

    def list(self) -> List[EquipmentModel]:
        return self.session.query(EquipmentModel).all()

    def update(self, data) -> EquipmentModel:
        m = self.session.query(EquipmentModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(EquipmentModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
