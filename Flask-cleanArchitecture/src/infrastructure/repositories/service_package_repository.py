from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.service_package_model import ServicePackageModel
from sqlalchemy import text

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

    def list_by_space(self, space_id: int) -> List[dict]:
        """Truy vấn các gói dịch vụ thuộc về một Space cụ thể qua bảng PackageDetails"""
        query = text("""
            SELECT 
                sp."PackageID", 
                sp."ProviderID", 
                sp."PackageName", 
                sp."Description", 
                sp."Price", 
                sp."Status", 
                sp."CreatedAt",
                pd."ReferenceID" AS "SpaceID"
            FROM "ServicePackages" sp
            JOIN "PackageDetails" pd 
                ON sp."PackageID" = pd."PackageID" AND pd."ItemType" = 'space'
            WHERE pd."ReferenceID" = :space_id AND sp."Status" = 'active'
        """)
        
        results = self.session.execute(query, {"space_id": space_id}).fetchall()
        
        output = []
        for row in results:
            item = dict(row._mapping)
            item['space_id'] = item.get('SpaceID')
            output.append(item)
            
        return output

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
