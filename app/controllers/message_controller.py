from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from fastapi.responses import JSONResponse

from ..schemas import message_schemas
from ..services import message_service
from ..utils import message_processor, rate_limiter
from .. import database

router = APIRouter(prefix='/api/messages', tags=['messages'])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    '/{session_id}',
    responses={
        200: {'model': message_schemas.MessageListOut},
        400: {'model': message_schemas.ErrorResponse}
    }
)
def get_messages(request: Request,
                       session_id: str,
                       db: Session = Depends(get_db),
                       limit: int = Query(50, ge=1),
                       offset: int = Query(0, ge=0),
                       sender: Optional[str] = Query(None),
                       message_search: Optional[str] = Query(None)):
    rate_limiter.rate_limiter(request)
    
    if sender and sender not in ('user', 'system'):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error": {
                    "code": "INVALID_FORMAT",
                    "message": "Formato de mensaje invalido",
                    "details": "El parametro 'sender' debe ser 'user' o 'system'"
                }
            }
        )
    
    total, messages = message_service.get_messages_by_session(session_id, db, limit, offset, sender, message_search)
    
    data = []
    for message in messages:
        data.append({
            "message_id": message.message_id,
            "session_id": message.session_id,
            "content": message.content,
            "timestamp": message.timestamp,
            "sender": message.sender,
            "metadata": {
                "word_count": message.word_count,
                "character_count": message.character_count,
                "processed_at": message.processed_at,
            }
        })
    
    return {
        'status': 'success',
        'total': total,
        'limit': limit,
        'offset': offset,
        'data': data
    }
    
    

@router.post(
    '/', 
    status_code=201,
    responses={
        201: {'model': message_schemas.MessageOut},
        400: {'model': message_schemas.ErrorResponse},
        409: {'model': message_schemas.ErrorResponse},
        500: {'model': message_schemas.ErrorResponse}
    }
)
def create_message(request: Request, 
                   payload:message_schemas.MessageCreate, 
                   db: Session = Depends(get_db)):
    rate_limiter.rate_limiter(request)
    
    cleaned_message, metadata = message_processor.process_message(payload.content)
    payload.content = cleaned_message
    
    try:
        message_created = message_service.create_message(payload, metadata, db)
    except IntegrityError:
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "error": {
                    "code": "DUPLICATE_ID",
                    "message": "El message_id ya existe",
                    "details": f"ID duplicado: {payload.message_id}"
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "status": "error",
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Error interno al guardar el mensaje",
                    "details": f"Error: {str(e)}"
                }
            }
        )
    
    return {
        'status': 'success',
        'data': {
            'message_id': message_created.message_id,
            "session_id": message_created.session_id,
            "content": message_created.content,
            "timestamp": message_created.timestamp,
            "sender": message_created.sender,
            "metadata": {
                "word_count": message_created.word_count,
                "character_count": message_created.character_count,
                "processed_at": message_created.processed_at
            }
        }
    }