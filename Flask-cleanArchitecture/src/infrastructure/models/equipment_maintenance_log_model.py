from sqlalchemy import Column, Integer, Date, String, Numeric, ForeignKey
from infrastructure.databases.base import Base

class EquipmentMaintenanceLogModel(Base):
    __tablename__ = 'EquipmentMaintenanceLogs'
    __table_args__ = {'extend_existing': True}

    id = Column('MaintenanceLogID', Integer, primary_key=True)
    equipment_id = Column('EquipmentID', Integer, ForeignKey('Equipment.EquipmentID'), nullable=False)
    maintenance_date = Column('MaintenanceDate', Date, nullable=False)
    description = Column('Description', String(255))
    cost = Column('Cost', Numeric(12,2))
    performed_by = Column('PerformedBy', String(255))
    next_scheduled_date = Column('NextScheduledDate', Date)
    status = Column('Status', String(30), nullable=False)
