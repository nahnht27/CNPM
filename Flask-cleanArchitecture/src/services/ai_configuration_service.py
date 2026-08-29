from typing import List


class AIConfigurationService:
    def __init__(self, repository):
        self.repository = repository

    def create_config(self, **data):
        return self.repository.add(data)

    def get_config(self, id: int):
        return self.repository.get_by_id(id)

    def list_configs(self) -> List:
        return self.repository.list()

    def update_config(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_config(self, id: int):
        return self.repository.delete(id)