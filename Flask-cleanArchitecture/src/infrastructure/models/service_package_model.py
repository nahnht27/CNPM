from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey
from infrastructure.databases.base import Base

class ServicePackageModel(Base):
    __tablename__ = 'ServicePackages'
    __table_args__ = {'extend_existing': True}

    id = Column('PackageID', Integer, primary_key=True)
    provider_id = Column('ProviderID', Integer, ForeignKey('ServiceProviders.ProviderID'), nullable=False)
    name = Column('PackageName', String(255), nullable=False)
    description = Column('Description', Text)
    price = Column('Price', Numeric(12,2), nullable=False)
    status = Column('Status', String(20), nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
