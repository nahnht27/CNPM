from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base

class SpaceImageModel(Base):
    __tablename__ = 'SpaceImages'
    __table_args__ = {'extend_existing': True}

    id = Column('SpaceImageID', Integer, primary_key=True)
    space_id = Column('SpaceID', Integer, ForeignKey('CreativeSpaces.SpaceID'), nullable=False)
    image_url = Column('ImageUrl', String(500), nullable=False)
    uploaded_at = Column('UploadedAt', DateTime, nullable=False)
