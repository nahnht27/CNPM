from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from infrastructure.databases.base import Base

class PostModel(Base):
    __tablename__ = 'Posts'
    __table_args__ = {'extend_existing': True}

    id = Column('PostID', Integer, primary_key=True)
    author_id = Column('AuthorID', Integer, ForeignKey('Users.UserID'), nullable=False)
    title = Column('Title', String(255), nullable=False)
    content = Column('Content', Text, nullable=False)
    category = Column('Category', String(30), nullable=False)
    status = Column('Status', String(30), nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
