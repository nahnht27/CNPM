from typing import List


class CreativeSpaceService:

    def __init__(self, repository):
        self.repository = repository

    def create_space(self, **data):
        return self.repository.add(data)

    def get_space(self, id: int):
        return self.repository.get_by_id(id)

    def get_space_detail(self, id: int):
        return self.repository.get_detail(id)

    def list_spaces(self) -> List:
        return self.repository.list()

    def update_space(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_space(self, id: int):
        return self.repository.delete(id)