from datetime import datetime
from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.notification_model import NotificationModel


class NotificationRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> NotificationModel:
        notification = NotificationModel(
            user_id=data.get('user_id'),
            title=data.get('title'),
            content=data.get('content'),
            type=data.get('type') or 'general',
            is_read=(
                data.get('is_read')
                if data.get('is_read') is not None
                else False
            ),
            created_at=(
                data.get('created_at')
                if data.get('created_at') is not None
                else datetime.utcnow()
            )
        )

        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)

        return notification

    def get_by_id(self, id: int) -> Optional[NotificationModel]:
        return self.session.query(NotificationModel).filter_by(id=id).first()

    def list(self) -> List[NotificationModel]:
        return (
            self.session.query(NotificationModel)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )

    def list_by_user(self, user_id: int) -> List[NotificationModel]:
        return (
            self.session.query(NotificationModel)
            .filter(NotificationModel.user_id == user_id)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )

    def count_unread_by_user(self, user_id: int) -> int:
        return (
            self.session.query(NotificationModel)
            .filter(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read.is_(False)
            )
            .count()
        )

    def mark_as_read(self, id: int) -> Optional[NotificationModel]:
        notification = (
            self.session.query(NotificationModel)
            .filter_by(id=id)
            .first()
        )

        if not notification:
            return None

        notification.is_read = True
        self.session.commit()
        self.session.refresh(notification)

        return notification

    def update(self, data) -> NotificationModel:
        notification = (
            self.session.query(NotificationModel)
            .filter_by(id=data.get('id'))
            .first()
        )

        if not notification:
            raise ValueError('Not found')

        for key, value in data.items():
            if hasattr(notification, key) and key != 'id':
                setattr(notification, key, value)

        self.session.commit()
        self.session.refresh(notification)

        return notification

    def delete(self, id: int) -> None:
        notification = (
            self.session.query(NotificationModel)
            .filter_by(id=id)
            .first()
        )

        if notification:
            self.session.delete(notification)
            self.session.commit()