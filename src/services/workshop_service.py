from typing import List

class WorkshopService:
    def __init__(self, repository):
        self.repository = repository

    def create_workshop(self, **data):
        return self.repository.add(data)

    def get_workshop(self, id: int):
        return self.repository.get_by_id(id)

    def list_workshops(self) -> List:
        return self.repository.list()

    def update_workshop(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_workshop(self, id: int):
        return self.repository.delete(id)
