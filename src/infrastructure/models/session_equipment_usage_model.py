from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base

class SessionEquipmentUsageModel(Base):
    __tablename__ = 'SessionEquipmentUsage'
    __table_args__ = {'extend_existing': True}

    id = Column('SEUsageID', Integer, primary_key=True)
    session_id = Column('SessionID', Integer, ForeignKey('ServiceSessions.SessionID'), nullable=False)
    equipment_id = Column('EquipmentID', Integer, ForeignKey('Equipment.EquipmentID'), nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    notes = Column('Notes', String(255))
