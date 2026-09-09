from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, String
from infrastructure.databases.base import Base
from datetime import datetime

class BookingModel(Base):
    __tablename__ = 'Bookings'
    __table_args__ = {'extend_existing': True}

    id = Column('BookingID', Integer, primary_key=True)
    photographer_id = Column('PhotographerID', Integer, ForeignKey('Users.UserID'), nullable=False)
    space_id = Column('SpaceID', Integer, ForeignKey('CreativeSpaces.SpaceID'), nullable=False)
    package_id = Column('PackageID', Integer, ForeignKey('ServicePackages.PackageID'))
    start_time = Column('StartTime', DateTime, nullable=False)
    end_time = Column('EndTime', DateTime, nullable=False)
    status = Column('Status', String(20), nullable=False)
    total_price = Column('TotalPrice', Numeric(12,2), nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False, default=datetime.now)
