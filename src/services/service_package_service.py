from typing import List

class ServicePackageService:
    def __init__(self, repository):
        self.repository = repository

    def create_package(self, **data):
        return self.repository.add(data)

    def get_package(self, id: int):
        return self.repository.get_by_id(id)

    def list_packages(self) -> List:
        return self.repository.list()

    def update_package(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_package(self, id: int):
        return self.repository.delete(id)
