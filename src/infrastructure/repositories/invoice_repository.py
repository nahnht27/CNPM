from typing import List, Optional
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.invoice_model import InvoiceModel

class InvoiceRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def add(self, data) -> InvoiceModel:
        m = InvoiceModel(
            session_id=data.get('session_id'),
            invoice_number=data.get('invoice_number'),
            subtotal=data.get('subtotal'),
            discount_amount=data.get('discount_amount'),
            tax_amount=data.get('tax_amount'),
            total_amount=data.get('total_amount'),
            issued_at=data.get('issued_at')
        )
        self.session.add(m)
        self.session.commit()
        self.session.refresh(m)
        return m

    def get_by_id(self, id: int) -> Optional[InvoiceModel]:
        return self.session.query(InvoiceModel).filter_by(id=id).first()

    def list(self) -> List[InvoiceModel]:
        return self.session.query(InvoiceModel).all()

    def update(self, data) -> InvoiceModel:
        m = self.session.query(InvoiceModel).filter_by(id=data.get('id')).first()
        if not m:
            raise ValueError('Not found')
        for k, v in data.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, v)
        self.session.commit()
        return m

    def delete(self, id: int) -> None:
        m = self.session.query(InvoiceModel).filter_by(id=id).first()
        if m:
            self.session.delete(m)
            self.session.commit()
