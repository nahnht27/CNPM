from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from infrastructure.databases.base import Base

class PostCommentModel(Base):
    __tablename__ = 'PostComments'
    __table_args__ = {'extend_existing': True}

    id = Column('CommentID', Integer, primary_key=True)
    post_id = Column('PostID', Integer, ForeignKey('Posts.PostID'), nullable=False)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), nullable=False)
    content = Column('Content', Text, nullable=False)
    created_at = Column('CreatedAt', DateTime, nullable=False)
