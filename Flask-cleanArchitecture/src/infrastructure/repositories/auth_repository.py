from domain.models.iauth_repository import IAuthRepository
from domain.models.auth import Auth

from typing import Optional
from datetime import datetime

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.auth.auth_user_model import AuthUserModel
from infrastructure.models.user_model import UserModel
from infrastructure.models.role_model import RoleModel

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash


class AuthRepository(IAuthRepository):

    def __init__(self):
        self.session: Session = (
            db_factory.get_database("POSTGREE").session
        )

    # =========================
    # LOGIN - DÙNG BẢNG Users
    # =========================
    def login(self, auth: Auth) -> Optional[Auth]:

        selected_user = (
            self.session.query(UserModel)
            .filter_by(username=auth.username)
            .first()
        )

        if not selected_user:
            return None

        if not check_password_hash(
            selected_user.password_hash,
            auth.password
        ):
            return None

        auth.id = selected_user.ID

        return auth

    # =========================
    # SIGNUP - GHI VÀO Users
    # =========================
    def register(self, auth: Auth) -> Optional[Auth]:

        try:
            # Lấy RoleID của Photographer
            role = (
                self.session.query(RoleModel)
                .filter_by(name="Photographer")
                .first()
            )

            if not role:
                return None

            new_user = UserModel(
                username=auth.username,
                password_hash=auth.password,

                # Request hiện tại không có full_name
                # nên dùng username làm giá trị mặc định
                full_name=auth.username,

                email=auth.email,
                created_at=datetime.utcnow(),
                status="active",
                role_id=role.ID
            )

            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)

            auth.id = new_user.ID

            return auth

        except Exception as e:
            self.session.rollback()
            print("REGISTER ERROR:", repr(e))
            return None

    # =========================
    # OTHER FUNCTIONS
    # =========================
    def remember_password(self):
        return None

    def look_account(self, user_id: int):
        return True

    def un_look_account(self, user_id: int):
        pass

    # =========================
    # CHECK EXIST - DÙNG Users
    # =========================
    def check_exist(self, username: str) -> bool:

        existing_user = (
            self.session.query(UserModel)
            .filter_by(username=username)
            .first()
        )

        return existing_user is not None