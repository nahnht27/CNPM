from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from infrastructure.databases.base import Base

class ConsumableModel(Base):
    __tablename__ = 'Consumables'
    __table_args__ = {'extend_existing': True}

    id = Column('ConsumableID', Integer, primary_key=True)
    provider_id = Column('ProviderID', Integer, ForeignKey('ServiceProviders.ProviderID'), nullable=False)
    name = Column('ConsumableName', String(255), nullable=False)
    type = Column('ConsumableType', String(255), nullable=False)
    unit = Column('Unit', String(20), nullable=False)
    stock_quantity = Column('StockQuantity', Numeric(10,2))
    unit_price = Column('UnitPrice', Numeric(12,2), nullable=False)
    expiry_date = Column('ExpiryDate', Date, nullable=False)
