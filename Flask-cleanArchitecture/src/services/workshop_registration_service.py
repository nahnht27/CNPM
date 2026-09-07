from datetime import datetime


class WorkshopRegistrationService:
    def __init__(self, repository, workshop_repository, notification_service):
        self.repository = repository
        self.workshop_repository = workshop_repository
        self.notification_service = notification_service

    def register(self, workshop_id: int, user_id: int):
        # 1. Check workshop exists
        workshop = self.workshop_repository.get_by_id(workshop_id)

        if not workshop:
            raise ValueError('Workshop not found')

        # 2. Check duplicate registration
        existing = self.repository.get_by_workshop_and_user(
            workshop_id,
            user_id
        )

        if existing:
            raise ValueError('User already registered for this workshop')

        # 3. Check workshop capacity
        registered_count = self.repository.count_by_workshop(workshop_id)

        if registered_count >= workshop.capacity:
            raise ValueError('Workshop is full')

        # 4. Create registration
        data = {
            'workshop_id': workshop_id,
            'user_id': user_id,
            'registered_at': datetime.utcnow(),
            'status': 'Registered'
        }

        registration = self.repository.add(data)

        # 5. Create notification for Photographer
        self.notification_service.create_notification(
            user_id=user_id,
            title='Đăng ký workshop thành công',
            content=f'Bạn đã đăng ký workshop "{workshop.title}" thành công.',
            type='workshop'
        )

        return registration

    def get_registration(self, id: int):
        return self.repository.get_by_id(id)

    def list_by_user(self, user_id: int):
        return self.repository.list_by_user(user_id)

    def list_by_workshop(self, workshop_id: int):
        return self.repository.list_by_workshop(workshop_id)