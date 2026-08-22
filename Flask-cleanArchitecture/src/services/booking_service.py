from typing import List

class BookingService:
    def __init__(self, repository):
        self.repository = repository

    def create_booking(self, **data):
        return self.repository.add(data)

    def get_booking(self, id: int):
        return self.repository.get_by_id(id)

    def list_bookings(self) -> List:
        return self.repository.list()

    def update_booking(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_booking(self, id: int):
        return self.repository.delete(id)
