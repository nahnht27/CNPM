from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base

class RoleModel(Base):
    __tablename__ = 'Roles'
    __table_args__ = {'extend_existing': True}

    ID = Column('RoleID', Integer, primary_key=True)
    name = Column('RoleName', String(255), nullable=False, unique=True)
    created_at = Column('CreatedAt', DateTime, nullable=False)
    created_by = Column('CreatedBy', Integer, ForeignKey('Users.UserID'), nullable=False)
    updated_at = Column('UpdatedAt', DateTime, nullable=False)
    updated_by = Column('UpdatedBy', Integer, ForeignKey('Users.UserID'), nullable=False)
