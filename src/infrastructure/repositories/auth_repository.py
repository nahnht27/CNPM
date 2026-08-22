from domain.models.iauth_repository import IAuthRepository
from domain.models.auth import Auth

from typing import  Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from sqlalchemy.orm import Session
from infrastructure.models.auth.auth_user_model import AuthUserModel
from infrastructure.models.user_model import UserModel



class AuthRepository(IAuthRepository):

    def __init__(self):
        self.session: Session = (
            db_factory.get_database("POSTGREE").session
        )

    def login(self, auth: Auth) -> Optional[Auth]:

        selected_user = (
            self.session.query(AuthUserModel)
            .filter_by(
                username=auth.username,
                password_hash=auth.password
            )
            .first()
        )

        if not selected_user:
            return None

        auth.id = selected_user.id

        return auth

    def register(self, auth: Auth) -> Optional[Auth]:

        try:

            new_user = AuthUserModel(
                username=auth.username,
                password_hash=auth.password,
                email=auth.email
            )

            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)

            auth.id = new_user.id

            return auth

        except Exception:

            self.session.rollback()

            return None

    def remember_password(self):

        return None

    def look_account(self, user_id: int):

        return True

    def un_look_account(self, user_id: int):

        pass

    def check_exist(self, username: str) -> bool:

        existing_user = (
            self.session.query(AuthUserModel)
            .filter_by(username=username)
            .first()
        )

        return existing_user is not None
    

