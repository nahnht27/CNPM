from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.workshop_registration_model import WorkshopRegistrationModel
from infrastructure.models.user_model import UserModel


class WorkshopRegistrationRepository:

    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session


    def add(self, data) -> WorkshopRegistrationModel:

        registration = WorkshopRegistrationModel(
            workshop_id=data.get('workshop_id'),
            user_id=data.get('user_id'),
            registered_at=data.get('registered_at'),
            status=data.get('status')
        )

        self.session.add(registration)
        self.session.commit()
        self.session.refresh(registration)

        return registration


    def get_by_id(
        self,
        id: int
    ) -> Optional[WorkshopRegistrationModel]:

        return (
            self.session
            .query(WorkshopRegistrationModel)
            .filter_by(id=id)
            .first()
        )


    def get_by_workshop_and_user(
        self,
        workshop_id: int,
        user_id: int
    ) -> Optional[WorkshopRegistrationModel]:

        return (
            self.session
            .query(WorkshopRegistrationModel)
            .filter_by(
                workshop_id=workshop_id,
                user_id=user_id
            )
            .first()
        )


    def count_by_workshop(
        self,
        workshop_id: int
    ) -> int:

        return (
            self.session
            .query(WorkshopRegistrationModel)
            .filter_by(
                workshop_id=workshop_id
            )
            .count()
        )


    def list_by_user(
        self,
        user_id: int
    ) -> List[WorkshopRegistrationModel]:

        return (
            self.session
            .query(WorkshopRegistrationModel)
            .filter_by(
                user_id=user_id
            )
            .all()
        )


    def list_by_workshop(
        self,
        workshop_id: int
    ):

        rows = (
            self.session
            .query(
                WorkshopRegistrationModel,
                UserModel
            )
            .join(
                UserModel,
                WorkshopRegistrationModel.user_id == UserModel.ID
            )
            .filter(
                WorkshopRegistrationModel.workshop_id == workshop_id
            )
            .all()
        )


        result = []

        for registration, user in rows:

            result.append({

                "workshop_registration_id":
                    registration.id,

                "workshop_id":
                    registration.workshop_id,

                "user_id":
                    registration.user_id,

                "username":
                    user.username,

                "full_name":
                    user.full_name,

                "email":
                    user.email,

                "phone":
                    user.phone,

                "avatar":
                    user.avatar,

                "registered_at":
                    registration.registered_at,

                "status":
                    registration.status

            })


        return result