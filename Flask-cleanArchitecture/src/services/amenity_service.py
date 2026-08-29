from typing import List


class AmenityService:
    def __init__(self, repository):
        self.repository = repository

    def create_amenity(self, **data):
        return self.repository.add(data)

    def get_amenity(self, id: int):
        return self.repository.get_by_id(id)

    def list_amenities(self) -> List:
        return self.repository.list()

    def update_amenity(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_amenity(self, id: int):
        return self.repository.delete(id)