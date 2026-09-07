from datetime import datetime
from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.service_package_model import ServicePackageModel
from infrastructure.models.package_detail_model import PackageDetailModel


class ServicePackageRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def _get_space_detail(self, package_id):
        return (
            self.session
            .query(PackageDetailModel)
            .filter(
                PackageDetailModel.package_id == package_id,
                PackageDetailModel.item_type == 'space'
            )
            .first()
        )

    def add(self, data) -> ServicePackageModel:
        m = ServicePackageModel(
            provider_id=data.get('provider_id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            status=data.get('status') or 'active',
            created_at=data.get('created_at') or datetime.utcnow()
        )

        self.session.add(m)
        self.session.flush()

        space_id = data.get('space_id')
        if space_id is not None:
            self.session.add(PackageDetailModel(
                package_id=m.id,
                item_type='space',
                reference_id=space_id,
                quantity=1
            ))

        self.session.commit()
        self.session.refresh(m)
        m.space_id = space_id
        return m

    def get_by_id(self, id: int) -> Optional[ServicePackageModel]:
        package = (
            self.session
            .query(ServicePackageModel)
            .filter_by(id=id)
            .first()
        )
        if package:
            detail = self._get_space_detail(package.id)
            package.space_id = detail.reference_id if detail else None
        return package

    def list(self) -> List[ServicePackageModel]:
        packages = self.session.query(ServicePackageModel).all()
        for package in packages:
            detail = self._get_space_detail(package.id)
            package.space_id = detail.reference_id if detail else None
        return packages

    def get_packages_by_space(self, space_id: int) -> List[ServicePackageModel]:
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
        for package in packages:
            package.space_id = space_id
        return packages

    def update(self, data) -> ServicePackageModel:
        package_id = data.get('id')
        m = (
            self.session
            .query(ServicePackageModel)
            .filter_by(id=package_id)
            .first()
        )

        if not m:
            raise ValueError('Not found')

        for k, v in data.items():
            if hasattr(m, k) and k not in ('id', 'space_id'):
                setattr(m, k, v)

        if not m.status:
            m.status = 'active'

        if 'space_id' in data:
            detail = self._get_space_detail(package_id)
            space_id = data.get('space_id')

            if space_id is None:
                if detail:
                    self.session.delete(detail)
            elif detail:
                detail.reference_id = space_id
                detail.quantity = 1
            else:
                self.session.add(PackageDetailModel(
                    package_id=package_id,
                    item_type='space',
                    reference_id=space_id,
                    quantity=1
                ))

            m.space_id = space_id

        self.session.commit()
        self.session.refresh(m)
        if not hasattr(m, 'space_id'):
            detail = self._get_space_detail(package_id)
            m.space_id = detail.reference_id if detail else None
        return m

    def delete(self, id: int) -> None:
        m = (
            self.session
            .query(ServicePackageModel)
            .filter_by(id=id)
            .first()
        )

        if not m:
            return

        details = (
            self.session
            .query(PackageDetailModel)
            .filter_by(package_id=id)
            .all()
        )
        for detail in details:
            self.session.delete(detail)

        self.session.delete(m)
        self.session.commit()
