from sqlalchemy import Column, Integer, Numeric, ForeignKey
from infrastructure.databases.base import Base

class BookingEquipmentModel(Base):
    __tablename__ = 'BookingEquipment'
    __table_args__ = {'extend_existing': True}

    id = Column('BookingEquipmentID', Integer, primary_key=True)
    booking_id = Column('BookingID', Integer, ForeignKey('Bookings.BookingID'), nullable=False)
    equipment_id = Column('EquipmentID', Integer, ForeignKey('Equipment.EquipmentID'), nullable=False)
    quantity = Column('Quantity', Integer)
    rental_price = Column('RentalPrice', Numeric(12,2), nullable=False)
