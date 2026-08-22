from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from infrastructure.databases.base import Base

class WorkshopModel(Base):
    __tablename__ = 'Workshops'
    __table_args__ = {'extend_existing': True}

    id = Column('WorkshopID', Integer, primary_key=True)
    provider_id = Column('ProviderID', Integer, ForeignKey('ServiceProviders.ProviderID'), nullable=False)
    title = Column('Title', String(255), nullable=False)
    description = Column('Description', Text)
    location = Column('Location', String(500), nullable=False)
    start_time = Column('StartTime', DateTime, nullable=False)
    end_time = Column('EndTime', DateTime, nullable=False)
    capacity = Column('Capacity', Integer, nullable=False)
    fee = Column('Fee', Numeric(12,2), nullable=False)
    status = Column('Status', String(20), nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
