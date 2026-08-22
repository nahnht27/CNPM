from sqlalchemy import Column, Integer, ForeignKey
from infrastructure.databases.base import Base

class SpaceAmenityModel(Base):
    __tablename__ = 'SpaceAmenities'
    __table_args__ = {'extend_existing': True}

    id = Column('SpaceAmenitiesID', Integer, primary_key=True)
    space_id = Column('SpaceID', Integer, ForeignKey('CreativeSpaces.SpaceID'), nullable=False)
    amenity_id = Column('AmenityID', Integer, ForeignKey('Amenities.AmenityID'), nullable=False)
