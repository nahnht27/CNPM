from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.user_model import UserModel


class UserRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> UserModel:
        user = UserModel(username=data.get('username'), password_hash=data.get('password_hash'), full_name=data.get('full_name'), email=data.get('email'), phone=data.get('phone'), avatar=data.get('avatar'), gender=data.get('gender'), created_at=data.get('created_at'), status=data.get('status'), role_id=data.get('role_id'))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.session.query(UserModel).filter_by(id=user_id).first()

    def list(self) -> List[UserModel]:
        return self.session.query(UserModel).all()

    def update(self, data) -> UserModel:
        user = self.session.query(UserModel).filter_by(id=data.get('id')).first()
        if not user:
            raise ValueError('User not found')
        for k, v in data.items():
            if hasattr(user, k) and k != 'id':
                setattr(user, k, v)
        self.session.commit()
        return user

    def delete(self, user_id: int) -> None:
        user = self.session.query(UserModel).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
    