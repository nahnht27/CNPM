from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.service_provider_model import ServiceProviderModel

class ServiceProviderRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> ServiceProviderModel:
        m = ServiceProviderModel(
            user_id=data.get('user_id'),
            business_name=data.get('business_name'),
            tax_code=data.get('tax_code'),
            business_address=data.get('business_address'),
            license_url=data.get('license_url'),
            verification_status=data.get('verification_status'),
            approved_at=data.get('approved_at'),
            bank_info=data.get('bank_info'),
            created_at=data.get('created_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[ServiceProviderModel]:
        return self.session.query(ServiceProviderModel).filter_by(id=id).first()

    def list(self) -> List[ServiceProviderModel]:
        return self.session.query(ServiceProviderModel).all()

    def update(self, data) -> ServiceProviderModel:
        m = self.session.query(ServiceProviderModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(ServiceProviderModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
