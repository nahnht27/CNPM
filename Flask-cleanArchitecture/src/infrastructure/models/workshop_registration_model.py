from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from infrastructure.databases.base import Base

class WorkshopRegistrationModel(Base):
    __tablename__ = 'WorkshopRegistrations'
    __table_args__ = {'extend_existing': True}

    id = Column('WorkshopRegistrationID', Integer, primary_key=True)
    workshop_id = Column('WorkshopID', Integer, ForeignKey('Workshops.WorkshopID'), nullable=False)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), nullable=False)
    registered_at = Column('RegisteredAt', DateTime, nullable=False)
    status = Column('Status', String(20), nullable=False)
