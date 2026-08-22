from typing import List

class PaymentService:
    def __init__(self, repository):
        self.repository = repository

    def create_payment(self, **data):
        return self.repository.add(data)

    def get_payment(self, id: int):
        return self.repository.get_by_id(id)

    def list_payments(self) -> List:
        return self.repository.list()

    def update_payment(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_payment(self, id: int):
        return self.repository.delete(id)
