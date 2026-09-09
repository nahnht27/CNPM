from typing import List

class ComplaintService:
    def __init__(self, repository):
        self.repository = repository

    def create_complaint(self, **data):
        return self.repository.add(data)

    def get_complaint(self, id: int):
        return self.repository.get_by_id(id)

    def list_complaints(self) -> List:
        return self.repository.list()

    def update_complaint(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_complaint(self, id: int):
        return self.repository.delete(id)
