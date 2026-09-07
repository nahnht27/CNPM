from datetime import datetime

from infrastructure.models.service_provider_model import ServiceProviderModel
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class WorkshopRegistrationService:
    def __init__(
        self,
        repository,
        workshop_repository,
        notification_service
    ):
        self.repository = repository
        self.workshop_repository = workshop_repository
        self.notification_service = notification_service

        # Dùng session PostgreSQL hiện tại của project
        self.session = db_factory.get_database('POSTGREE').session

    def register(self, workshop_id: int, user_id: int):
        # =====================================================
        # 1. Check workshop exists
        # =====================================================

        workshop = self.workshop_repository.get_by_id(
            workshop_id
        )

        if not workshop:
            raise ValueError('Workshop not found')


        # =====================================================
        # 2. Check duplicate registration
        # =====================================================

        existing = self.repository.get_by_workshop_and_user(
            workshop_id,
            user_id
        )

        if existing:
            raise ValueError(
                'User already registered for this workshop'
            )


        # =====================================================
        # 3. Check workshop capacity
        # =====================================================

        registered_count = self.repository.count_by_workshop(
            workshop_id
        )

        if registered_count >= workshop.capacity:
            raise ValueError(
                'Workshop is full'
            )


        # =====================================================
        # 4. Create registration
        # =====================================================

        data = {
            'workshop_id': workshop_id,
            'user_id': user_id,
            'registered_at': datetime.utcnow(),
            'status': 'Registered'
        }

        registration = self.repository.add(
            data
        )


        # =====================================================
        # 5. Notification for Photographer
        # =====================================================

        try:

            self.notification_service.create_notification(

                user_id=user_id,

                title='Đăng ký workshop thành công',

                content=(
                    f'Bạn đã đăng ký workshop '
                    f'"{workshop.title}" thành công.'
                ),

                type='workshop'

            )

        except Exception as notification_error:

            print(
                'PHOTOGRAPHER NOTIFICATION ERROR:',
                notification_error
            )


        # =====================================================
        # 6. Find Provider
        #
        # Workshops.ProviderID
        #        ↓
        # ServiceProviders.ProviderID
        #        ↓
        # ServiceProviders.UserID
        # =====================================================

        provider = (
            self.session.query(ServiceProviderModel)
            .filter(
                ServiceProviderModel.id ==
                workshop.provider_id
            )
            .first()
        )


        # =====================================================
        # 7. Notification for Provider
        # =====================================================

        if provider:

            try:

                self.notification_service.create_notification(

                    user_id=provider.user_id,

                    title='Có người đăng ký workshop',

                    content=(
                        f'Một photographer vừa đăng ký '
                        f'workshop "{workshop.title}" '
                        f'của bạn.'
                    ),

                    type='workshop'

                )

            except Exception as notification_error:

                print(
                    'PROVIDER NOTIFICATION ERROR:',
                    notification_error
                )


        # =====================================================
        # 8. Return registration
        # =====================================================

        return registration


    def get_registration(self, id: int):

        return self.repository.get_by_id(
            id
        )


    def list_by_user(self, user_id: int):

        return self.repository.list_by_user(
            user_id
        )


    def list_by_workshop(self, workshop_id: int):

        return self.repository.list_by_workshop(
            workshop_id
        )