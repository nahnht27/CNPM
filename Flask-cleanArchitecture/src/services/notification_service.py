from typing import List


class NotificationService:

    def __init__(self, repository):
        self.repository = repository


    def create_notification(self, **data):

        return self.repository.add(data)


    def get_notification(
        self,
        id: int
    ):

        return self.repository.get_by_id(id)


    def list_notifications(self) -> List:

        return self.repository.list()


    def list_user_notifications(
        self,
        user_id: int
    ) -> List:

        return self.repository.list_by_user(
            user_id
        )


    def count_unread(
        self,
        user_id: int
    ) -> int:

        return self.repository.count_unread_by_user(
            user_id
        )


    def mark_as_read(
        self,
        id: int
    ):

        return self.repository.mark_as_read(
            id
        )


    def update_notification(
        self,
        id: int,
        **data
    ):

        data['id'] = id

        return self.repository.update(
            data
        )


    def delete_notification(
        self,
        id: int
    ):

        return self.repository.delete(
            id
        )