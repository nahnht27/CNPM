from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.service_package_model import ServicePackageModel

class ServicePackageRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> ServicePackageModel:
        m = ServicePackageModel(
            provider_id=data.get('provider_id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            status=data.get('status'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[ServicePackageModel]:
        return self.session.query(ServicePackageModel).filter_by(id=id).first()

    def list(self) -> List[ServicePackageModel]:
        return self.session.query(ServicePackageModel).all()

    def update(self, data) -> ServicePackageModel:
        m = self.session.query(ServicePackageModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(ServicePackageModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
