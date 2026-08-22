from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from infrastructure.databases.base import Base

class InvoiceModel(Base):
    __tablename__ = 'Invoices'
    __table_args__ = {'extend_existing': True}

    id = Column('InvoiceID', Integer, primary_key=True)
    session_id = Column('SessionID', Integer, ForeignKey('ServiceSessions.SessionID'), nullable=False, unique=True)
    invoice_number = Column('InvoiceNumber', String(50), nullable=False, unique=True)
    subtotal = Column('SubTotal', Numeric(12,2), nullable=False)
    discount_amount = Column('DiscountAmount', Numeric(12,2))
    tax_amount = Column('TaxAmount', Numeric(12,2))
    total_amount = Column('TotalAmount', Numeric(12,2), nullable=False)
    issued_at = Column('IssuedAt', DateTime, nullable=False)
