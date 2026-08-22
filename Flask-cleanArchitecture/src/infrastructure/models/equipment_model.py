from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from infrastructure.databases.base import Base

class EquipmentModel(Base):
    __tablename__ = 'Equipment'
    __table_args__ = {'extend_existing': True}

    id = Column('EquipmentID', Integer, primary_key=True)
    provider_id = Column('ProviderID', Integer, ForeignKey('ServiceProviders.ProviderID'), nullable=False)
    space_id = Column('SpaceID', Integer, ForeignKey('CreativeSpaces.SpaceID'))
    category_id = Column('CategoryID', Integer, ForeignKey('Categories.CategoryID'), nullable=False)
    name = Column('EquipmentName', String(255), nullable=False)
    brand = Column('Brand', String(100))
    condition = Column('Condition', String(30), nullable=False)
    rental_price = Column('RentalPrice', Numeric(12,2), nullable=False)
    status = Column('Status', String(20), nullable=False)
    purchase_date = Column('PurchaseDate', DateTime, nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
