from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from infrastructure.databases.base import Base

class UserModel(Base):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}

    ID = Column('UserID', Integer, primary_key=True)
    username = Column('UserName', String(100), nullable=False, unique=True)
    password_hash = Column('PasswordHash', String(255), nullable=False)
    full_name = Column('FullName', String(255), nullable=False)
    email = Column('Email', String(255), nullable=False, unique=True)
    phone = Column('Phone', String(20), unique=True)
    avatar = Column('Avatar', String(255))
    gender = Column('Gender', String(255))
    created_at = Column('CreatedAt', DateTime, nullable=False)
    status = Column('Status', String(30), nullable=False)
    role_id = Column('RoleID', Integer, ForeignKey('Roles.RoleID'), nullable=False)