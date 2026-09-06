from typing import List, Optional
from datetime import datetime


class PaymentService:

    PAYMENT_METHOD = 'Chuyển khoản QR (VietQR)'

    SUCCESS = 'Thành công'
    FAILED = 'Thất bại'
    PENDING = 'Đang chờ xử lý'
    REFUNDED = 'Đã hoàn tiền'

    ALLOWED_STATUSES = {
        SUCCESS,
        FAILED,
        PENDING,
        REFUNDED
    }

    def __init__(self, repository, invoice_repository=None):
        self.repository = repository
        self.invoice_repository = invoice_repository

    # ==========================================================
    # GET ALL PAYMENTS
    # ==========================================================
    def list_payments(self) -> List:
        return self.repository.list()

    # ==========================================================
    # GET PAYMENT BY ID
    # ==========================================================
    def get_payment(self, pay_id: int):
        return self.repository.get_by_id(pay_id)

    # ==========================================================
    # GET PAYMENT BY INVOICE ID
    # ==========================================================
    def get_payment_by_invoice(self, invoice_id: int):
        return self.repository.get_by_invoice_id(invoice_id)

    # ==========================================================
    # CREATE PAYMENT (TỰ ĐỘNG THÀNH CÔNG)
    # ==========================================================
    def create_payment(self, **data):
        invoice_id = data.get('invoice_id', 0)
        payment_amount = data.get('amount')

        if payment_amount is None:
            raise ValueError('amount là bắt buộc')

        # TỰ ĐỘNG TẠO INVOICE NẾU CHƯA CÓ INVOICE_ID HOẶC INVOICE_ID == 0
        if invoice_id is None or int(invoice_id) == 0:
            if not self.invoice_repository:
                raise ValueError('InvoiceRepository chưa được cấu hình')

            session_id = data.get('session_id') or 1
            discount_amount = data.get('discount_amount', 0)
            tax_amount = data.get('tax_amount', 0)

            new_invoice_payload = {
                'SessionID': int(session_id),
                'InvoiceNumber': f"INV-{int(datetime.now().timestamp())}",
                'SubTotal': float(payment_amount),
                'DiscountAmount': float(discount_amount),
                'TaxAmount': float(tax_amount),
                'TotalAmount': float(payment_amount),
                'IssuedAt': datetime.now()
            }

            try:
                invoice = self.invoice_repository.add(**new_invoice_payload)
            except TypeError:
                invoice = self.invoice_repository.add(new_invoice_payload)

            created_invoice_id = (
                getattr(invoice, 'InvoiceID', None) 
                or getattr(invoice, 'invoice_id', None)
                or getattr(invoice, 'id', None)
            )
            if isinstance(invoice, dict):
                created_invoice_id = (
                    invoice.get('InvoiceID') 
                    or invoice.get('invoice_id') 
                    or invoice.get('id')
                )

            if not created_invoice_id:
                raise ValueError('Tạo Invoice thất bại, không nhận được InvoiceID từ database')

            invoice_id = created_invoice_id
            data['invoice_id'] = invoice_id

        # TỰ ĐỘNG CHUYỂN TRẠNG THÁI SANG THÀNH CÔNG
        data['payment_method'] = data.get('payment_method') or self.PAYMENT_METHOD
        data['status'] = self.SUCCESS
        data['paid_at'] = datetime.now()

        return self.repository.add(data)

    # ==========================================================
    # UPDATE PAYMENT
    # ==========================================================
    def update_payment(self, pay_id: int, **data):
        status = data.get('status')
        if status and status not in self.ALLOWED_STATUSES:
            raise ValueError(f'Trạng thái không hợp lệ. Chỉ chấp nhận: {", ".join(self.ALLOWED_STATUSES)}')

        payload = {'id': pay_id, **data}
        if status == self.SUCCESS and 'paid_at' not in payload:
            payload['paid_at'] = datetime.now()

        return self.repository.update(payload)

    # ==========================================================
    # DELETE PAYMENT
    # ==========================================================
    def delete_payment(self, pay_id: int) -> bool:
        return self.repository.delete(pay_id)