from typing import List

class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, **data):
        return self.repository.add(data)

    def get_category(self, id: int):
        return self.repository.get_by_id(id)

    def list_categories(self) -> List:
        return self.repository.list()

    def update_category(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_category(self, id: int):
        return self.repository.delete(id)
