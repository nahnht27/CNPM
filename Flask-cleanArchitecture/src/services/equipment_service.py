from typing import List


class EquipmentService:
    def __init__(self, repository):
        self.repository = repository

    def create_equipment(self, **data):
        return self.repository.add(data)

    def get_equipment(self, id: int):
        return self.repository.get_by_id(id)

    def list_equipment(self, space_id: int = None) -> List:
        items = self.repository.list()

        if space_id is not None:
            items = [item for item in items if getattr(item, 'SpaceID', None) == space_id]

        return items

    def update_equipment(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_equipment(self, id: int):
        return self.repository.delete(id)