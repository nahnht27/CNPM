from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey
)

from infrastructure.databases.base import Base


class PaymentModel(Base):

    __tablename__ = 'Payments'

    __table_args__ = {
        'extend_existing': True
    }

    id = Column(
        'PaymentID',
        Integer,
        primary_key=True,
        autoincrement=True
    )

    invoice_id = Column(
        'InvoiceID',
        Integer,
        ForeignKey('Invoices.InvoiceID'),
        nullable=False
    )

    payment_method = Column(
        'PaymentMethod',
        String(255),
        nullable=False
    )

    amount = Column(
        'Amount',
        Numeric(12, 2),
        nullable=False
    )

    # Đặt giá trị mặc định khi INSERT vào DB là 'Đang chờ xử lý'
    # Đăng ký độ dài String(50) để tránh bị cắt chuỗi Tiếng Việt
    status = Column(
        'Status',
        String(50),
        default='Đang chờ xử lý',
        nullable=False
    )

    # Payment mới tạo chưa được Provider duyệt nên để NULL
    paid_at = Column(
        'PaidAt',
        DateTime,
        nullable=True
    )