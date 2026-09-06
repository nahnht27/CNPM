from typing import List
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

    def __init__(
        self,
        repository,
        invoice_repository=None
    ):

        self.repository = repository
        self.invoice_repository = invoice_repository

    # ==========================================================
    # CREATE PAYMENT
    # ==========================================================

    def create_payment(self, **data):

        invoice_id = data.get('invoice_id')

        if not invoice_id:
            raise ValueError(
                'invoice_id là bắt buộc'
            )

        # ------------------------------------------------------
        # Kiểm tra Invoice
        # ------------------------------------------------------

        if self.invoice_repository:

            invoice = (
                self.invoice_repository
                .get_by_id(invoice_id)
            )

            if not invoice:

                raise ValueError(
                    'Không tìm thấy Invoice'
                )

            invoice_amount = invoice.total_amount

            payment_amount = data.get('amount')

            if payment_amount is None:

                raise ValueError(
                    'amount là bắt buộc'
                )

            if float(payment_amount) != float(
                invoice_amount
            ):

                raise ValueError(
                    'Số tiền thanh toán không khớp '
                    'với tổng tiền hóa đơn'
                )

        # ------------------------------------------------------
        # Kiểm tra phương thức thanh toán
        # ------------------------------------------------------

        payment_method = data.get(
            'payment_method'
        )

        if payment_method != self.PAYMENT_METHOD:

            raise ValueError(
                'Phương thức thanh toán không hợp lệ. '
                'Chỉ hỗ trợ Chuyển khoản QR (VietQR)'
            )

        # ------------------------------------------------------
        # Kiểm tra Payment hiện tại
        # ------------------------------------------------------

        existing = (
            self.repository
            .get_by_invoice_id(invoice_id)
        )

        if existing:

            if existing.status == self.SUCCESS:

                raise ValueError(
                    'Invoice này đã được thanh toán'
                )

            if existing.status == self.PENDING:

                raise ValueError(
                    'Invoice này đã có một Payment '
                    'đang chờ xác nhận'
                )

        # ------------------------------------------------------
        # Photographer tạo Payment
        #
        # Chưa xác nhận đã nhận tiền.
        # ------------------------------------------------------

        data['payment_method'] = (
            self.PAYMENT_METHOD
        )

        data['status'] = self.PENDING

        data['paid_at'] = None

        return self.repository.add(data)

    # ==========================================================
    # GET BY ID
    # ==========================================================

    def get_payment(
        self,
        id: int
    ):

        return self.repository.get_by_id(id)

    # ==========================================================
    # GET BY INVOICE
    # ==========================================================

    def get_payment_by_invoice(
        self,
        invoice_id: int
    ):

        return (
            self.repository
            .get_by_invoice_id(invoice_id)
        )

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list_payments(self) -> List:

        return self.repository.list()

    # ==========================================================
    # UPDATE PAYMENT
    # ==========================================================

    def update_payment(
        self,
        id: int,
        **data
    ):

        payment = (
            self.repository
            .get_by_id(id)
        )

        if not payment:
            return None

        # ------------------------------------------------------
        # Không cho đổi phương thức thanh toán
        # ------------------------------------------------------

        if 'payment_method' in data:

            if (
                data['payment_method']
                != self.PAYMENT_METHOD
            ):

                raise ValueError(
                    'Phương thức thanh toán không hợp lệ. '
                    'Chỉ hỗ trợ Chuyển khoản QR (VietQR)'
                )

        # ------------------------------------------------------
        # Kiểm tra status
        # ------------------------------------------------------

        if 'status' in data:

            if (
                data['status']
                not in self.ALLOWED_STATUSES
            ):

                raise ValueError(
                    'Trạng thái thanh toán không hợp lệ'
                )

        # ------------------------------------------------------
        # Payment đã thành công
        # không cho quay lại trạng thái khác
        # ------------------------------------------------------

        if payment.status == self.SUCCESS:

            if data.get('status') != self.SUCCESS:

                raise ValueError(
                    'Payment đã được xác nhận thành công '
                    'và không thể thay đổi trạng thái'
                )

        # ------------------------------------------------------
        # Provider xác nhận đã nhận tiền
        # ------------------------------------------------------

        if data.get('status') == self.SUCCESS:

            data['paid_at'] = datetime.now()

        # ------------------------------------------------------
        # Payment pending
        # ------------------------------------------------------

        elif data.get('status') == self.PENDING:

            data['paid_at'] = None

        # ------------------------------------------------------
        # Payment failed
        # ------------------------------------------------------

        elif data.get('status') == self.FAILED:

            data['paid_at'] = None

        # ------------------------------------------------------
        # ID
        # ------------------------------------------------------

        data['id'] = id

        return self.repository.update(data)

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_payment(
        self,
        id: int
    ):

        return self.repository.delete(id)