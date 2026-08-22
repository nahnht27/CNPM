from sqlalchemy import Column, Integer, Numeric, ForeignKey, Text
from infrastructure.databases.base import Base


class InvoiceDetailModel(Base):
    __tablename__ = 'InvoiceDetail'
    __table_args__ = {'extend_existing': True}

    id = Column('InvoiceDetailID', Integer, primary_key=True)
    invoice_id = Column('InvoiceID', Integer, ForeignKey('Invoices.InvoiceID'), nullable=False)
    description = Column('Description', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    unit_price = Column('UnitPrice', Numeric(12,2), nullable=False)
    line_total = Column('LineTotal', Numeric(12,2), nullable=False)
