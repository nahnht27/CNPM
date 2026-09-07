from typing import List, Optional

from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.invoice_model import InvoiceModel


class InvoiceRepository:

    def __init__(self, session=None):
        self.session = (
            session
            or db_factory.get_database('POSTGREE').session
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def add(self, data) -> InvoiceModel:

        model = InvoiceModel(
            session_id=data.get('session_id'),
            invoice_number=data.get('invoice_number'),
            subtotal=data.get('subtotal'),
            discount_amount=data.get('discount_amount'),
            tax_amount=data.get('tax_amount'),
            total_amount=data.get('total_amount'),
            issued_at=data.get('issued_at')
        )

        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)

            return model

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # GET BY ID
    # ==========================================================

    def get_by_id(
        self,
        id: int
    ) -> Optional[InvoiceModel]:

        return (
            self.session.query(InvoiceModel)
            .filter_by(id=id)
            .first()
        )

    # ==========================================================
    # GET BY SERVICE SESSION
    # ==========================================================

    def get_by_session_id(
        self,
        session_id: int
    ) -> Optional[InvoiceModel]:

        return (
            self.session.query(InvoiceModel)
            .filter_by(session_id=session_id)
            .first()
        )

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list(self) -> List[InvoiceModel]:

        return (
            self.session
            .query(InvoiceModel)
            .all()
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        data
    ) -> Optional[InvoiceModel]:

        model = (
            self.session.query(InvoiceModel)
            .filter_by(id=data.get('id'))
            .first()
        )

        if not model:
            return None

        try:

            for key, value in data.items():

                if hasattr(model, key) and key != 'id':
                    setattr(model, key, value)

            self.session.commit()
            self.session.refresh(model)

            return model

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        id: int
    ) -> bool:

        model = (
            self.session.query(InvoiceModel)
            .filter_by(id=id)
            .first()
        )

        if not model:
            return False

        try:

            self.session.delete(model)
            self.session.commit()

            return True

        except Exception:
            self.session.rollback()
            raise