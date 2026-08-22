from typing import List

class ReviewService:
    def __init__(self, repository):
        self.repository = repository

    def create_review(self, **data):
        return self.repository.add(data)

    def get_review(self, id: int):
        return self.repository.get_by_id(id)

    def list_reviews(self) -> List:
        return self.repository.list()

    def update_review(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_review(self, id: int):
        return self.repository.delete(id)
