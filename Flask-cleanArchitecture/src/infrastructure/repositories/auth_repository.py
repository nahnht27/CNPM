from domain.models.iauth_repository import IAuthRepository
from domain.models.auth import Auth

from typing import Optional
from datetime import datetime

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.auth.auth_user_model import AuthUserModel
from infrastructure.models.user_model import UserModel
from infrastructure.models.role_model import RoleModel
from infrastructure.models.service_provider_model import ServiceProviderModel

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash


class AuthRepository(IAuthRepository):

    def __init__(self):
        self.session: Session = (
            db_factory.get_database("POSTGREE").session
        )

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self, auth: Auth) -> Optional[Auth]:

        # Tìm user theo username
        selected_user = (
            self.session
            .query(UserModel)
            .filter_by(username=auth.username)
            .first()
        )

        if not selected_user:
            return None

        # Kiểm tra password
        if not check_password_hash(
            selected_user.password_hash,
            auth.password
        ):
            return None

        # Gán thông tin User
        auth.id = selected_user.ID
        auth.role_id = selected_user.role_id

        # =====================================================
        # Nếu là Service Provider thì lấy ProviderID
        # RoleID = 3 -> Service Provider
        # =====================================================

        if selected_user.role_id == 3:

            provider = (
                self.session
                .query(ServiceProviderModel)
                .filter_by(user_id=selected_user.ID)
                .first()
            )

            if provider:
                auth.provider_id = provider.id

        return auth

    # =========================================================
    # SIGN UP
    # =========================================================

    def register(self, auth: Auth) -> Optional[Auth]:

        try:

            # Kiểm tra Role
            role = (
                self.session
                .query(RoleModel)
                .filter_by(ID=auth.role_id)
                .first()
            )

            if not role:
                return None

            # Tạo User mới
            new_user = UserModel(
                username=auth.username,
                password_hash=auth.password,

                # Request hiện tại chưa có full_name
                # nên dùng username
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

            print(
                "REGISTER ERROR:",
                repr(e)
            )

            return None

    # =========================================================
    # REMEMBER PASSWORD
    # =========================================================

    def remember_password(self):
        return None

    # =========================================================
    # LOCK ACCOUNT
    # =========================================================

    def look_account(self, user_id: int):
        return True

    # =========================================================
    # UNLOCK ACCOUNT
    # =========================================================

    def un_look_account(self, user_id: int):
        pass

    # =========================================================
    # CHECK EXIST USER
    # =========================================================

    def check_exist(self, username: str) -> bool:

        existing_user = (
            self.session
            .query(UserModel)
            .filter_by(username=username)
            .first()
        )

        return existing_user is not None

    # =========================================================
    # GET USER BY EMAIL
    # =========================================================

    def get_by_email(self, email: str):

        return (
            self.session
            .query(UserModel)
            .filter_by(email=email)
            .first()
        )

    # =========================================================
    # UPDATE PASSWORD
    # =========================================================

    def update_password(
        self,
        user_id: int,
        password_hash: str
    ) -> bool:

        try:

            user = (
                self.session
                .query(UserModel)
                .filter_by(ID=user_id)
                .first()
            )

            if not user:
                return False

            user.password_hash = password_hash

            self.session.commit()

            return True

        except Exception as e:

            self.session.rollback()

            print(
                "UPDATE PASSWORD ERROR:",
                repr(e)
            )

            return False