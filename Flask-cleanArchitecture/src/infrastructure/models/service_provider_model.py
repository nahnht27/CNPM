from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from infrastructure.databases.base import Base

class ServiceProviderModel(Base):
    __tablename__ = 'ServiceProviders'
    __table_args__ = {'extend_existing': True}

    id = Column('ProviderID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), nullable=False, unique=True)
    business_name = Column('BusinessName', String(255), nullable=False)
    tax_code = Column('TaxCode', String(50), unique=True)
    business_address = Column('BusinessAddress', String(500), nullable=False)
    license_url = Column('LicenseUrl', String(500), nullable=False)
    verification_status = Column('VerificationStatus', String(20), nullable=False)
    approved_at = Column('ApprovedAt', DateTime)
    bank_info = Column('Bank_Info', String(500))
    created_at = Column('CreatedAt', DateTime, nullable=False)
