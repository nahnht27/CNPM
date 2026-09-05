from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.service_package_model import ServicePackageModel
from infrastructure.models.package_detail_model import PackageDetailModel


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
        return (
            self.session
            .query(ServicePackageModel)
            .filter_by(id=id)
            .first()
        )

    def list(self) -> List[ServicePackageModel]:
        packages = (
            self.session
            .query(ServicePackageModel)
            .all()
        )

        # Gắn space_id vào object để ResponseSchema có thể trả về
        for package in packages:
            detail = (
                self.session
                .query(PackageDetailModel)
                .filter(
                    PackageDetailModel.package_id == package.id,
                    PackageDetailModel.item_type == 'space'
                )
                .first()
            )

            package.space_id = detail.reference_id if detail else None

        return packages

    def get_packages_by_space(
        self,
        space_id: int
    ) -> List[ServicePackageModel]:

        packages = (
            self.session
            .query(ServicePackageModel)
            .join(
                PackageDetailModel,
                ServicePackageModel.id == PackageDetailModel.package_id
            )
            .filter(
                PackageDetailModel.item_type == 'space',
                PackageDetailModel.reference_id == space_id
            )
            .all()
        )

        # Cho Schema biết package này thuộc SpaceID nào
        for package in packages:
            package.space_id = space_id

        return packages

    def update(self, data) -> ServicePackageModel:
        m = (
            self.session
            .query(ServicePackageModel)
            .filter_by(id=data.get('id'))
            .first()
        )

        if not m:
            raise ValueError('Not found')

        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)

        self.session.commit()

        return m

    def delete(self, id: int) -> None:
        m = (
            self.session
            .query(ServicePackageModel)
            .filter_by(id=id)
            .first()
        )

        if m:
            self.session.delete(m)
            self.session.commit()