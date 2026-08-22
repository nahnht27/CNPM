from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base

class AmenityModel(Base):
    __tablename__ = 'Amenities'
    __table_args__ = {'extend_existing': True}

    id = Column('AmenityID', Integer, primary_key=True)
    name = Column('AmenitieName', String(255), nullable=False, unique=True)
