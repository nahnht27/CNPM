from typing import List
from datetime import datetime


class InvoiceService:

    def __init__(self, repository):
        self.repository = repository

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_invoice(self, **data):

        session_id = data.get('session_id')

        if not session_id:
            raise ValueError('session_id là bắt buộc')

        # Mỗi ServiceSession chỉ có một Invoice
        existing = self.repository.get_by_session_id(
            session_id
        )

        if existing:
            return existing

        # Tự sinh invoice number nếu không truyền vào
        if not data.get('invoice_number'):
            data['invoice_number'] = (
                f'INV-{session_id:06d}'
            )

        # Các giá trị tiền
        subtotal = data.get('subtotal', 0)
        discount_amount = data.get(
            'discount_amount',
            0
        )
        tax_amount = data.get(
            'tax_amount',
            0
        )

        # Tính tổng tiền
        data['total_amount'] = (
            subtotal
            - discount_amount
            + tax_amount
        )

        # Tự tạo thời gian xuất hóa đơn
        if not data.get('issued_at'):
            data['issued_at'] = datetime.now()

        return self.repository.add(data)

    # ==========================================================
    # GET BY ID
    # ==========================================================

    def get_invoice(self, id: int):

        return self.repository.get_by_id(id)

    # ==========================================================
    # GET BY SESSION
    # ==========================================================

    def get_invoice_by_session(
        self,
        session_id: int
    ):

        return self.repository.get_by_session_id(
            session_id
        )

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list_invoices(self) -> List:

        return self.repository.list()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_invoice(
        self,
        id: int,
        **data
    ):

        data['id'] = id

        return self.repository.update(data)

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_invoice(self, id: int):

        return self.repository.delete(id)