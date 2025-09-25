from app.services import message_service
from app.models.message_model import Message
from app.schemas.message_schemas import MessageCreate
from datetime import datetime, timezone
from typing import List

MESSAGE_BODY = MessageCreate(
    message_id = "msg-123456",
    session_id = "session-abcdef",
    content = "Hola, ¿cómo puedo ayudarte hoy?",
    timestamp = "2023-06-15T14:30:00Z",
    sender = "system"
)
MESSAGE_METADATA = {
    'word_count': 5,
    'character_count': 31,
    'processed_at': datetime.now(timezone.utc)
}
MESSAGE_BODY_2 = MessageCreate(
    message_id = "msg-123457",
    session_id = "session-abcdef",
    content = "Buenos dias, sera que me puedes responder unas preguntas sobre xyz?",
    timestamp = "2023-06-15T14:32:00Z",
    sender = "user"
)
MESSAGE_METADATA_2 = {
    'word_count': 11,
    'character_count': 67,
    'processed_at': datetime.now(timezone.utc)
}

def test_create_new_message_inserts_into_db(db):    
    created = message_service.create_message(MESSAGE_BODY, MESSAGE_METADATA, db)
    
    assert isinstance(created, Message)
    message_saved = db.query(Message).filter_by(message_id = MESSAGE_BODY.message_id).first()
    assert message_saved is not None
    assert message_saved.content == MESSAGE_BODY.content
    
def test_get_messages_filtered_by_session(db):
    message_service.create_message(MESSAGE_BODY, MESSAGE_METADATA, db)
    
    total, messages = message_service.get_messages_by_session(
        MESSAGE_BODY.session_id, 
        db=db, 
        limit=1, 
        offset=0, 
        sender=None,
        message_search=None
    )
    
    assert total == 1
    assert total == len(messages)
    assert isinstance(messages, List)
    assert messages[0].message_id == MESSAGE_BODY.message_id

def test_get_messages_filtered_by_sender(db):
    message_service.create_message(MESSAGE_BODY, MESSAGE_METADATA, db)
    message_service.create_message(MESSAGE_BODY_2, MESSAGE_METADATA_2, db)
    
    total, messages = message_service.get_messages_by_session(
        MESSAGE_BODY.session_id, 
        db=db, 
        limit=1, 
        offset=0, 
        sender='user',
        message_search=None
    )
    
    assert total == 1
    assert total == len(messages)
    assert messages[0].sender == 'user'

def test_get_messages_filtered_by_message(db):
    message_service.create_message(MESSAGE_BODY, MESSAGE_METADATA, db)
    message_service.create_message(MESSAGE_BODY_2, MESSAGE_METADATA_2, db)
    
    total, messages = message_service.get_messages_by_session(
        MESSAGE_BODY.session_id, 
        db=db, 
        limit=1, 
        offset=0, 
        sender=None,
        message_search='hola'
    )
    
    assert total == 1
    assert total == len(messages)
    assert messages[0].content == MESSAGE_BODY.content