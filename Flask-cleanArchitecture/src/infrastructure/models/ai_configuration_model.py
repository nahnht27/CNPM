from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from infrastructure.databases.base import Base

class AIConfigurationModel(Base):
    __tablename__ = 'AIConfigurations'
    __table_args__ = {'extend_existing': True}

    id = Column('AIConfigID', Integer, primary_key=True)
    config_key = Column('ConfigKey', String(100), nullable=False, unique=True)
    config_value = Column('ConfigValue', String(255), nullable=False)
    is_active = Column('IsActive', Boolean, nullable=False)
    updated_at = Column('UpdatedAt', DateTime, nullable=False)
    updated_by = Column('UpdatedBy', Integer, ForeignKey('Users.UserID'), nullable=False)
