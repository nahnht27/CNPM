from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String
from infrastructure.databases.base import Base

class ReviewModel(Base):
    __tablename__ = 'Reviews'
    __table_args__ = {'extend_existing': True}

    id = Column('ReviewID', Integer, primary_key=True)
    photographer_id = Column('PhotographerID', Integer, ForeignKey('Users.UserID'), nullable=False)
    booking_id = Column('BookingID', Integer, ForeignKey('Bookings.BookingID'), nullable=False)
    target_type = Column('TargetType', String(20), nullable=False)
    target_id = Column('TargetID', Integer, nullable=False)
    rating = Column('Rating', Integer, nullable=False)
    comment = Column('Comment', Text)
    created_at = Column('CreatedAt', DateTime, nullable=False)
