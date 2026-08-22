from typing import List

class ServiceProviderService:
    def __init__(self, repository):
        self.repository = repository

    def create_provider(self, **data):
        return self.repository.add(data)

    def get_provider(self, id: int):
        return self.repository.get_by_id(id)

    def list_providers(self) -> List:
        return self.repository.list()

    def update_provider(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_provider(self, id: int):
        return self.repository.delete(id)
