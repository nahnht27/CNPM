from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from infrastructure.databases.base import Base

class ServiceSessionModel(Base):
    __tablename__ = 'ServiceSessions'
    __table_args__ = {'extend_existing': True}

    id = Column('SessionID', Integer, primary_key=True)
    booking_id = Column('BookingID', Integer, ForeignKey('Bookings.BookingID'), nullable=False, unique=True)
    check_in_time = Column('CheckInTime', DateTime)
    check_out_time = Column('CheckOutTime', DateTime)
    check_in_method = Column('CheckInMethod', String(20))
    actual_duration_minutes = Column('ActualDurationMinutes', Integer)
    notes = Column('Notes', Text)
    status = Column('Status', String(20), nullable=False)
