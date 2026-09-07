from typing import List, Optional
from infrastructure.databases.factory_database import (
    FactoryDatabase as db_factory
)
from infrastructure.models.payment_model import PaymentModel


class PaymentRepository:

    def __init__(self, session=None):
        self.session = (
            session
            or db_factory.get_database('POSTGREE').session
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def add(self, data=None, **kwargs) -> PaymentModel:
        if isinstance(data, PaymentModel):
            model = data
        else:
            payload = data if isinstance(data, dict) else kwargs

            # Ép kiểu dữ liệu an toàn tránh lỗi SQLAlchemy
            invoice_id = payload.get('invoice_id') or payload.get('InvoiceID')
            amount = payload.get('amount')
            
            model = PaymentModel(
                invoice_id=int(invoice_id) if invoice_id is not None else None,
                payment_method=str(payload.get('payment_method', '')),
                amount=float(amount) if amount is not None else 0.0,
                status=str(payload.get('status', 'Đang chờ xử lý')),
                paid_at=payload.get('paid_at')
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

    def get_by_id(self, id: int) -> Optional[PaymentModel]:
        return (
            self.session
            .query(PaymentModel)
            .filter_by(id=id)
            .first()
        )

    # ==========================================================
    # GET BY INVOICE
    # ==========================================================

    def get_by_invoice_id(self, invoice_id: int) -> Optional[PaymentModel]:
        return (
            self.session
            .query(PaymentModel)
            .filter_by(invoice_id=invoice_id)
            .first()
        )

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list(self) -> List[PaymentModel]:
        return (
            self.session
            .query(PaymentModel)
            .all()
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(self, data) -> Optional[PaymentModel]:
        pay_id = data.get('id') if isinstance(data, dict) else getattr(data, 'id', None)

        model = (
            self.session
            .query(PaymentModel)
            .filter_by(id=pay_id)
            .first()
        )

        if not model:
            return None

        try:
            if isinstance(data, dict):
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

    def delete(self, id: int) -> bool:
        model = (
            self.session
            .query(PaymentModel)
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