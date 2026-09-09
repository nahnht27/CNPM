from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from infrastructure.databases.base import Base

class PackageDetailModel(Base):
    __tablename__ = 'PackageDetails'
    __table_args__ = {'extend_existing': True}

    id = Column('PackageDetailID', Integer, primary_key=True)
    package_id = Column('PackageID', Integer, ForeignKey('ServicePackages.PackageID'), nullable=False)
    item_type = Column('ItemType', String(255), nullable=False)
    reference_id = Column('ReferenceID', Integer, nullable=False)
    quantity = Column('Quantity', Numeric(10,2), nullable=False)
