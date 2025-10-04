from pydantic import BaseModel, validator
from typing import Literal, Dict, Any, Optional
from datetime import datetime

class MessageIn(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: Literal['user', 'system']

    @validator('message_id', 'session_id', 'content', 'sender')
    def not_empty(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError('must not be empty')
        return v

class MessageOut(BaseModel):
    status: str
    data: Dict[str, Any]

class MessagesListOut(BaseModel):
    status: str
    data: list
    pagination: Dict[str, int]
