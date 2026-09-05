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
        # Truyền tách biệt id và dict data vào repository
        return self.repository.update(id, data)

    def delete_booking(self, id: int):
        return self.repository.delete(id)