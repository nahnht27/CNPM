from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from infrastructure.databases.base import Base

class PromotionModel(Base):
    __tablename__ = 'Promotions'
    __table_args__ = {'extend_existing': True}

    id = Column('PromotionID', Integer, primary_key=True)
    provider_id = Column('ProviderID', Integer, ForeignKey('ServiceProviders.ProviderID'), nullable=False)
    package_id = Column('PackageID', Integer, ForeignKey('ServicePackages.PackageID'))
    code = Column('Code', String(50), nullable=False)
    discount_type = Column('DiscountType', String(20), nullable=False)
    discount_value = Column('DiscountValue', Numeric(12,2), nullable=False)
    start_date = Column('StartDate', DateTime, nullable=False)
    end_date = Column('EndDate', DateTime, nullable=False)
    usage_limit = Column('UsageLimit', Integer)
    status = Column('Status', String(20), nullable=False)
