from typing import List

class PromotionService:
    def __init__(self, repository):
        self.repository = repository

    def create_promotion(self, **data):
        return self.repository.add(data)

    def get_promotion(self, id: int):
        return self.repository.get_by_id(id)

    def list_promotions(self) -> List:
        return self.repository.list()

    def update_promotion(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_promotion(self, id: int):
        return self.repository.delete(id)
