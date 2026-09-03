from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.user_model import UserModel


class UserRepository:

    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return (
            self.session
            .query(UserModel)
            .filter(UserModel.ID == user_id)
            .first()
        )

    def update(self, user_id: int, data: dict) -> UserModel:

        user = self.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        allowed_fields = [
            "full_name",
            "email",
            "phone",
            "avatar"
        ]

        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        self.session.commit()
        self.session.refresh(user)

        return user