from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from infrastructure.databases.base import Base

class NotificationModel(Base):
    __tablename__ = 'Notifications'
    __table_args__ = {'extend_existing': True}

    id = Column('NotificationID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), nullable=False)
    title = Column('Title', String(255), nullable=False)
    content = Column('Content', Text, nullable=False)
    type = Column('Type', String(30), nullable=False)
    is_read = Column('IsRead', Boolean, nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
