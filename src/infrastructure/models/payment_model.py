from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from infrastructure.databases.base import Base

class PaymentModel(Base):
    __tablename__ = 'Payments'
    __table_args__ = {'extend_existing': True}

    id = Column('PaymentID', Integer, primary_key=True)
    invoice_id = Column('InvoiceID', Integer, ForeignKey('Invoices.InvoiceID'), nullable=False)
    payment_method = Column('PaymentMethod', String(255), nullable=False)
    amount = Column('Amount', Numeric(12,2), nullable=False)
    status = Column('Status', String(20), nullable=False)
    paid_at = Column('PaidAt', DateTime, nullable=False)
