from typing import List, Optional

class GenericService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, data: dict):
        return self.repository.add(data)

    def get(self, id: int):
        return self.repository.get_by_id(id)

    def list(self) -> List:
        return self.repository.list()

    def update(self, id: int, data: dict):
        data['id'] = id
        return self.repository.update(data)

    def delete(self, id: int):
        return self.repository.delete(id)
