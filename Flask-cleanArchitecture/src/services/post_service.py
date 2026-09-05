from typing import List

class PostService:
    def __init__(self, repository):
        self.repository = repository

    def create_post(self, **data):
        return self.repository.add(data)

    def get_post(self, id: int):
        return self.repository.get_by_id(id)

    def list_posts(self) -> List:
        return self.repository.list()

    def update_post(self, id: int, **data):
        data['id'] = id 
        return self.repository.update(data)

    def delete_post(self, id: int):
        return self.repository.delete(id)
