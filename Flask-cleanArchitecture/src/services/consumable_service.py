from typing import List


class ConsumableService:

    def __init__(self, repository):
        self.repository = repository

    def create_consumable(self, **data):
        return self.repository.add(data)

    def get_consumable(self, id: int):
        return self.repository.get_by_id(id)

    def list_consumables(self) -> List:
        return self.repository.list()

    def update_consumable(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_consumable(self, id: int):
        return self.repository.delete(id)