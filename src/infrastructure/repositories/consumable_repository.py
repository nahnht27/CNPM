from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.consumable_model import ConsumableModel


class ConsumableRepository:

    def __init__(self, session=None):
        self.session = session or db_factory.get_database(
            'POSTGREE'
        ).session

    def add(self, data) -> ConsumableModel:
        model = ConsumableModel(
            provider_id=data.get('provider_id'),
            name=data.get('name'),
            consumable_type=data.get('consumable_type'),
            unit=data.get('unit'),
            stock_quantity=data.get('stock_quantity'),
            unit_price=data.get('unit_price'),
            expiry_date=data.get('expiry_date')
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return model

    def get_by_id(self, id: int) -> Optional[ConsumableModel]:
        return (
            self.session
            .query(ConsumableModel)
            .filter_by(id=id)
            .first()
        )

    def list(self) -> List[ConsumableModel]:
        return (
            self.session
            .query(ConsumableModel)
            .all()
        )

    def update(self, data) -> ConsumableModel:
        model = (
            self.session
            .query(ConsumableModel)
            .filter_by(id=data.get('id'))
            .first()
        )

        if not model:
            raise ValueError('Không tìm thấy vật tư tiêu hao')

        for key, value in data.items():
            if hasattr(model, key) and key != 'id':
                setattr(model, key, value)

        self.session.commit()
        self.session.refresh(model)

        return model

    def delete(self, id: int) -> None:
        model = (
            self.session
            .query(ConsumableModel)
            .filter_by(id=id)
            .first()
        )

        if model:
            self.session.delete(model)
            self.session.commit()