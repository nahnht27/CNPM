from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.role_model import RoleModel

class RoleRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> RoleModel:
        role = RoleModel(name=data.get('name'), created_at=data.get('created_at'), created_by=data.get('created_by'))
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def get_by_id(self, role_id: int) -> Optional[RoleModel]:
        return self.session.query(RoleModel).filter_by(id=role_id).first()

    def list(self) -> List[RoleModel]:
        return self.session.query(RoleModel).all()

    def update(self, data) -> RoleModel:
        role = self.session.query(RoleModel).filter_by(id=data.get('id')).first()
        if not role:
            raise ValueError('Role not found')
        if data.get('name') is not None:
            role.name = data.get('name')
        role.updated_at = data.get('updated_at')
        role.updated_by = data.get('updated_by')
        self.session.commit()
        return role

    def delete(self, role_id: int) -> None:
        role = self.session.query(RoleModel).filter_by(id=role_id).first()
        if role:
            self.session.delete(role)
            self.session.commit()
