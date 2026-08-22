from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from infrastructure.databases.base import Base

class ComplaintModel(Base):
    __tablename__ = 'Complaints'
    __table_args__ = {'extend_existing': True}

    id = Column('ComplaintID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), nullable=False)
    booking_id = Column('BookingID', Integer, ForeignKey('Bookings.BookingID'))
    target_type = Column('TargetType', String(20), nullable=False)
    target_id = Column('TargetID', Integer, nullable=False)
    description = Column('Description', Text, nullable=False)
    status = Column('Status', String(20), nullable=False)
    resolved_at = Column('ResolvedAt', DateTime)
