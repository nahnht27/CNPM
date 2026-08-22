from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from infrastructure.databases.base import Base

class AIInteractionLogModel(Base):
    __tablename__ = 'AIInteractionLogs'
    __table_args__ = {'extend_existing': True}

    id = Column('AIInteractionLogID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), nullable=False)
    interaction_type = Column('InteractionType', String(30), nullable=False)
    query_text = Column('QueryText', Text)
    response_text = Column('ResponseText', Text)
    created_at = Column('CreatedAt', DateTime, nullable=False)
