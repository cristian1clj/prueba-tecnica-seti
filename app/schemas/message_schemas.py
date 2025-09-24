from pydantic import BaseModel, field_validator
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    
    @field_validator('sender')
    @classmethod
    def check_sender(cls, v):
        if v not in ('user', 'system'):
            raise ValueError("El campo 'sender' debe ser 'user' o 'system'")
        return v
    
class MessageCreate(MessageBase):
    pass

class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime

class MessageOut(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: MessageMetadata
    
class MessageListOut(BaseModel):
    status: str
    total: int
    limit: int
    offset: int
    data: list[MessageOut]
    
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    error: ErrorDetail