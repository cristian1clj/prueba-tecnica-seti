from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from ..models import message_model
import json

def create_message(message_data, metadata, db: Session):
    message = message_model.Message(
        message_id = message_data.message_id,
        session_id = message_data.session_id,
        content = message_data.content,
        timestamp = message_data.timestamp,
        sender = message_data.sender,
        word_count = metadata['word_count'],
        character_count = metadata['character_count'],
        processed_at = metadata['processed_at']
    )
    db.add(message)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(message)
    return message

def get_messages_by_session(session_id: str, 
                            db: Session, 
                            limit: int, 
                            offset: int, 
                            sender: str | None,
                            message_search: str | None):
    messages = db.query(message_model.Message).filter(message_model.Message.session_id == session_id)
    if sender:
        messages = messages.filter(message_model.Message.sender == sender)
    
    if message_search:
        messages = messages.filter(message_model.Message.content.like(f"%{message_search}%"))
        
    total = messages.count()
    res = messages.order_by(message_model.Message.timestamp.asc()).offset(offset).limit(limit).all()
    return total, res