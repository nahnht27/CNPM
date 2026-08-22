from sqlalchemy import Column, Integer, Numeric, ForeignKey
from infrastructure.databases.base import Base

class SessionConsumableUsageModel(Base):
    __tablename__ = 'SessionConsumableUsage'
    __table_args__ = {'extend_existing': True}

    id = Column('SCUsageID', Integer, primary_key=True)
    session_id = Column('SessionID', Integer, ForeignKey('ServiceSessions.SessionID'), nullable=False)
    consumable_id = Column('ConsumableID', Integer, ForeignKey('Consumables.ConsumableID'), nullable=False)
    quantity_used = Column('QuantityUsed', Numeric(10,2), nullable=False)
    cost = Column('Cost', Numeric(12,2), nullable=False)
