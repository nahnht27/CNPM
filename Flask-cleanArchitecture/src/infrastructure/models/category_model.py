from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base

class CategoryModel(Base):
    __tablename__ = 'Categories'
    __table_args__ = {'extend_existing': True}

    id = Column('CategoryID', Integer, primary_key=True)
    name = Column('CategoryName', String(100), nullable=False)
    description = Column('Description', String(255), nullable=False)
    category_type = Column('CategoryType', String(50), nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
