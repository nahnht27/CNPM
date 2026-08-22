from typing import List

class EquipmentService:
    def __init__(self, repository):
        self.repository = repository

    def create_equipment(self, **data):
        return self.repository.add(data)

    def get_equipment(self, id: int):
        return self.repository.get_by_id(id)

    def list_equipment(self) -> List:
        return self.repository.list()

    def update_equipment(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_equipment(self, id: int):
        return self.repository.delete(id)
