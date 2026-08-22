from typing import List

class InvoiceService:
    def __init__(self, repository):
        self.repository = repository

    def create_invoice(self, **data):
        return self.repository.add(data)

    def get_invoice(self, id: int):
        return self.repository.get_by_id(id)

    def list_invoices(self) -> List:
        return self.repository.list()

    def update_invoice(self, id: int, **data):
        data['id'] = id
        return self.repository.update(data)

    def delete_invoice(self, id: int):
        return self.repository.delete(id)
