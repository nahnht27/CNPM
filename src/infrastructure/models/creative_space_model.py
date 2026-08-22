from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey
from infrastructure.databases.base import Base

class CreativeSpaceModel(Base):
    __tablename__ = 'CreativeSpaces'
    __table_args__ = {'extend_existing': True}

    id = Column('SpaceID', Integer, primary_key=True)
    provider_id = Column('ProviderID', Integer, ForeignKey('ServiceProviders.ProviderID'), nullable=False)
    name = Column('SpaceName', String(255), nullable=False)
    category_id = Column('CategoryID', Integer, ForeignKey('Categories.CategoryID'), nullable=False)
    description = Column('Description', Text)
    size_sqm = Column('SizeSqm', Numeric(8,2))
    max_capacity = Column('MaxCapacity', Integer, nullable=False)
    operating_hours = Column('OperatingHours', String(100), nullable=False)
    pricing_model = Column('PricingModel', String(30), nullable=False)
    base_price = Column('BasePrice', Numeric(12,2), nullable=False)
    status = Column('Status', String(20), nullable=False)
    address = Column('Address', String(500), nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
