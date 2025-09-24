from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from ..database import Base

class Message(Base):
    __tablename__ = 'messages'
    
    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    character_count = Column(Integer, nullable=False)
    processed_at = Column(DateTime, nullable=False)